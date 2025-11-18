"""
Celery Configuration
Async task processing for scraping and email sending
"""
from celery import Celery
from config import Config

# Create Celery app
celery = Celery(
    'phd_automator',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

# Configure Celery
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Auto-discover tasks
celery.autodiscover_tasks(['tasks'])

if __name__ == '__main__':
    celery.start()
