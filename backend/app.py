# /backend/app.py

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import os
import uuid
from werkzeug.utils import secure_filename  # <-- FIX 1
from flask_socketio import SocketIO, join_room

from config import Config
from models import db, Product, Webhook
from celery_app import celery

# --- App Initialization ---
app = Flask(__name__)
app.config.from_object(Config)

# --- Create upload folder ---
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Extensions Initialization ---
db.init_app(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

# --- Initialize SocketIO ---
socketio = SocketIO(app, message_queue=app.config['REDIS_URL'], cors_allowed_origins="*")

# --- Link Flask config to Celery ---
celery.conf.update(app.config)

# --- Helper Functions ---
def parse_bool(value):
    """Helper to parse boolean strings from query args."""
    return str(value).lower() in ['true', '1', 't', 'yes']

# --- SocketIO Event Handler ---
@socketio.on('join_room')
def on_join(data):
    job_id = data['job_id']
    join_room(job_id)
    print(f"--- Client joined room: {job_id} ---")

# --- API Routes ---

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

# === STORY 1: File Upload ===
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        job_id = str(uuid.uuid4())
        
        # --- FIX 2: Call task by name ---
        celery.send_task('tasks.process_csv_import', args=[filepath, job_id])
        
        return jsonify({'job_id': job_id}), 202

# === STORY 2: Product Management UI ===

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    if not data or not data.get('sku') or not data.get('name'):
        return jsonify({'error': 'SKU and Name are required'}), 400

    new_product = Product(
        sku=data['sku'],
        name=data['name'],
        description=data.get('description'),
        active=data.get('active', True)
    )
    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'A product with this SKU already exists.'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    query = Product.query
    if 'sku' in request.args:
        query = query.filter(Product.sku.ilike(f"%{request.args['sku']}%"))
    if 'name' in request.args:
        query = query.filter(Product.name.ilike(f"%{request.args['name']}%"))
    if 'description' in request.args:
        query = query.filter(Product.description.ilike(f"%{request.args['description']}%"))
    if 'active' in request.args:
        query = query.filter(Product.active == parse_bool(request.args['active']))

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    
    return jsonify({
        'products': [p.to_dict() for p in products],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total_pages': pagination.pages
    })

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    try:
        product.sku = data.get('sku', product.sku)
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.active = data.get('active', product.active)
        db.session.commit()
        return jsonify(product.to_dict()), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'A product with this SKU already exists.'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# === STORY 3: Bulk Delete ===
@app.route('/api/products/delete-all', methods=['DELETE'])
def delete_all_products():
    job_id = str(uuid.uuid4())
    # --- FIX 3: Call task by name ---
    celery.send_task('tasks.bulk_delete_all_products', args=[job_id])
    return jsonify({'message': 'Bulk delete task started.', 'job_id': job_id}), 202


# === STORY 4: Webhook Configuration ===
@app.route('/api/webhooks', methods=['POST'])
def create_webhook():
    data = request.json
    if not data or not data.get('url'):
        return jsonify({'error': 'URL is required'}), 400
    new_webhook = Webhook(
        url=data['url'],
        event_type=data.get('event_type', 'product_update'),
        enabled=data.get('enabled', True)
    )
    db.session.add(new_webhook)
    db.session.commit()
    return jsonify(new_webhook.to_dict()), 201

@app.route('/api/webhooks', methods=['GET'])
def get_webhooks():
    webhooks = Webhook.query.all()
    return jsonify([w.to_dict() for w in webhooks])

@app.route('/api/webhooks/<int:id>', methods=['PUT'])
def update_webhook(id):
    webhook = Webhook.query.get_or_404(id)
    data = request.json
    webhook.url = data.get('url', webhook.url)
    webhook.event_type = data.get('event_type', webhook.event_type)
    webhook.enabled = data.get('enabled', webhook.enabled)
    db.session.commit()
    return jsonify(webhook.to_dict()), 200

@app.route('/api/webhooks/<int:id>', methods=['DELETE'])
def delete_webhook(id):
    webhook = Webhook.query.get_or_404(id)
    db.session.delete(webhook)
    db.session.commit()
    return jsonify({'message': 'Webhook deleted successfully.'}), 200

@app.route('/api/webhooks/test/<int:id>', methods=['POST'])
def test_webhook(id):
    webhook = Webhook.query.get_or_404(id)
    print(f"--- Firing TEST for Webhook {id}: {webhook.url} ---")
    return jsonify({
        'message': 'Test event triggered.',
        'dummy_response': { 'status': 200, 'body': 'OK' }
    }), 200

# --- Main entry point ---
if __name__ == '__main__':
    # --- FIX 4: Run with socketio ---
    print("--- Starting SocketIO server with eventlet ---")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)