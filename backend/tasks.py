from celery_app import celery, redis_url
from app import app, db
from models import Product
import pandas as pd
import os
from flask_socketio import SocketIO
from sqlalchemy import text
from celery.signals import task_prerun

socketio_client = SocketIO(message_queue=redis_url)

# This signal handler ensures that every Celery task gets a fresh
# database connection, preventing deadlocks from forked processes.
@task_prerun.connect
def on_task_prerun(*args, **kwargs):
    """Dispose of the engine connection pool before each task."""
    with app.app_context():
        db.engine.dispose()


@celery.task
def bulk_delete_all_products(job_id):
    with app.app_context():
        try:
            num_rows_deleted = db.session.query(Product).delete()
            db.session.commit()
            print(f"--- Bulk Delete: Deleted {num_rows_deleted} products. ---")
            
            socketio_client.emit('task_complete',
                                 {'status': f'Successfully deleted {num_rows_deleted} products.'},
                                 room=job_id)
            
        except Exception as e:
            db.session.rollback()
            print(f"--- Bulk Delete Error: {e} ---")
            
            socketio_client.emit('task_failed',
                                 {'error': str(e)},
                                 room=job_id)

@celery.task(bind=True)
def process_csv_import(self, filepath, job_id):
    with app.app_context():
        print(f"--- [Job {job_id}]: Starting CSV processing for {filepath} ---")
        
        try:
            total_rows = 500000
            
            socketio_client.emit('progress_update',
                                 {'status': 'Parsing CSV...', 'progress': 0},
                                 room=job_id)
            
            rows_processed = 0
            chunksize = 100
            
            # --- NEW: Commit counter ---
            chunk_counter = 0

            print(f"--- [Job {job_id}]: Starting pandas read_csv loop with chunksize={chunksize} ---")

            for chunk in pd.read_csv(filepath, chunksize=chunksize, engine='python'):
                chunk_counter += 1
                
                print(f"--- [Job {job_id}]: Processing one chunk of {len(chunk)} rows... ---")

                chunk.rename(columns=str.lower, inplace=True)
                chunk = chunk.where(pd.notnull(chunk), None)
                if 'sku' not in chunk.columns:
                    raise Exception("CSV is missing 'sku' column")
                
                chunk['sku'] = chunk['sku'].str.lower()
                records = chunk.to_dict('records')
                
                if not records: continue

                insert_stmt = """
                    INSERT INTO product (name, sku, description, active)
                    VALUES (:name, :sku, :description, true)
                    ON CONFLICT (lower(sku)) DO UPDATE SET
                        name = EXCLUDED.name,
                        description = EXCLUDED.description;
                """
                
                print(f"--- [Job {job_id}]: Inserting {len(records)} rows into DB session... ---")
                
                db.session.execute(text(insert_stmt), records)
                
                # --- NEW: Commit every 10 chunks (1000 rows) ---
                if chunk_counter % 10 == 0:
                    print(f"--- [Job {job_id}]: Committing batch of 1000 rows... ---")
                    db.session.commit()
                    print(f"--- [Job {job_id}]: Batch commit complete. ---")
                
                rows_processed += len(records)
                progress = (rows_processed / total_rows) * 100
                
                socketio_client.emit('progress_update',
                                     {'status': 'Importing...', 'progress': round(progress)},
                                     room=job_id)

            # --- NEW: Commit any remaining chunks ---
            print(f"--- [Job {job_id}]: Committing final batch... ---")
            db.session.commit()
            print(f"--- [Job {job_id}]: Final commit complete. ---")
            
            print(f"--- [Job {job_id}]: Finished pandas read_csv loop. ---")
            print(f"--- [Job {job_id}]: Import complete. ---")

            socketio_client.emit('task_complete',
                                 {'status': f'Import successful! {rows_processed} records processed.'},
                                 room=job_id)

        except Exception as e:
            db.session.rollback()
            print(f"--- [Job {job_id}]: FAILED. Error: {e} ---")
            
            socketio_client.emit('task_failed',
                                 {'error': str(e)},
                                 room=job_id)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"--- [Job {job_id}]: Cleaned up {filepath} ---")