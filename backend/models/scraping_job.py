"""
ScrapingJob Model
Tracks web scraping jobs and their progress
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from . import db


class ScrapingJob(db.Model):
    """ScrapingJob model for tracking scraping operations"""

    __tablename__ = 'scraping_jobs'

    # Status enum values
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_PAUSED = 'paused'

    # Job type enum values
    TYPE_UNIVERSITIES = 'universities'
    TYPE_PROFESSORS = 'professors'
    TYPE_SCHOLARSHIPS = 'scholarships'
    TYPE_PUBLICATIONS = 'publications'

    # Primary Key
    id = Column(Integer, primary_key=True)

    # Job Information
    job_type = Column(String(50), nullable=False, index=True)
    job_name = Column(String(255))
    description = Column(Text)

    # Parameters
    parameters = Column(JSON)  # Search parameters (countries, domains, etc.)
    target_count = Column(Integer)  # Expected number of items to scrape

    # Status and Progress
    status = Column(String(50), default=STATUS_PENDING, index=True)
    progress = Column(Integer, default=0)  # 0-100 percentage
    current_item = Column(String(500))  # Currently processing item

    # Results
    results_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    results_summary = Column(JSON)  # Summary of scraped data

    # Error Information
    error_message = Column(Text)
    error_details = Column(JSON)  # Detailed error information
    failed_items = Column(JSON)  # List of items that failed

    # Performance Metrics
    items_per_second = Column(Float)
    estimated_time_remaining = Column(Integer)  # Seconds

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, index=True)
    completed_at = Column(DateTime)
    cancelled_at = Column(DateTime)

    # Celery Task ID (for async jobs)
    celery_task_id = Column(String(255), index=True)

    def to_dict(self):
        """Convert scraping job to dictionary"""
        return {
            'id': self.id,
            'job_type': self.job_type,
            'job_name': self.job_name,
            'description': self.description,
            'parameters': self.parameters or {},
            'target_count': self.target_count,
            'status': self.status,
            'progress': self.progress,
            'current_item': self.current_item,
            'results_count': self.results_count,
            'success_count': self.success_count,
            'failed_count': self.failed_count,
            'results_summary': self.results_summary or {},
            'error_message': self.error_message,
            'items_per_second': self.items_per_second,
            'estimated_time_remaining': self.estimated_time_remaining,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'celery_task_id': self.celery_task_id,
        }

    def update_progress(self, progress, current_item=None, commit=True):
        """Update job progress"""
        self.progress = min(100, max(0, progress))
        if current_item:
            self.current_item = current_item

        if commit:
            db.session.commit()

    def mark_started(self, commit=True):
        """Mark job as started"""
        self.status = self.STATUS_RUNNING
        self.started_at = datetime.utcnow()

        if commit:
            db.session.commit()

    def mark_completed(self, commit=True):
        """Mark job as completed"""
        self.status = self.STATUS_COMPLETED
        self.completed_at = datetime.utcnow()
        self.progress = 100

        if commit:
            db.session.commit()

    def mark_failed(self, error_message, commit=True):
        """Mark job as failed"""
        self.status = self.STATUS_FAILED
        self.error_message = error_message
        self.completed_at = datetime.utcnow()

        if commit:
            db.session.commit()

    def __repr__(self):
        return f'<ScrapingJob {self.id} - {self.job_type} - {self.status}>'
