"""
Celery Tasks Package
"""
from .scraping_tasks import scrape_universities_task, scrape_professors_task
from .email_tasks import send_email_batch_task, send_single_email_task

__all__ = [
    'scrape_universities_task',
    'scrape_professors_task',
    'send_email_batch_task',
    'send_single_email_task'
]
