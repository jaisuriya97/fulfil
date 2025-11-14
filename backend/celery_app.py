# /backend/celery_app.py

from celery import Celery
import os
from dotenv import load_dotenv  # <-- Important

# Load environment variables from .env file
load_dotenv()                    # <-- Important

# Get Redis URL from environment, with a local fallback
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery(
    'product_importer',  # Name of your app
    broker=redis_url,
    backend=redis_url,
    include=['tasks']  # Tells Celery to look for tasks in 'tasks.py'
)

# Optional: Add timezone
celery.conf.timezone = 'UTC'