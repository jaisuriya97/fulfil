from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery(
    'product_importer',
    broker=redis_url,
    backend=redis_url,
    include=['tasks']
)

celery.conf.timezone = 'UTC'