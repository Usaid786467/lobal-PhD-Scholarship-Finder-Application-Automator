"""
Analytics Model for PhD Application Automator
Tracks metrics, statistics, and user activity
"""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Analytics(Base):
    """Analytics model for tracking metrics and statistics"""

    __tablename__ = 'analytics'

    id = Column(Integer, primary_key=True)

    # User Association
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Metric Information
    metric_name = Column(String(255), nullable=False, index=True)
    metric_category = Column(String(100), index=True)  # 'email', 'application', 'discovery', 'system'
    metric_value = Column(Float)
    metric_value_int = Column(Integer)
    metric_value_str = Column(String(500))

    # Date Information
    date = Column(Date, default=date.today, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Additional Data
    metadata = Column(JSON, default=dict)  # Extra information about the metric

    # Context
    context = Column(String(255))  # Where this metric came from
    entity_type = Column(String(100))  # 'university', 'professor', 'email', etc.
    entity_id = Column(Integer)  # ID of related entity

    def to_dict(self):
        """Convert analytics entry to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'metric_name': self.metric_name,
            'metric_category': self.metric_category,
            'metric_value': self.metric_value,
            'metric_value_int': self.metric_value_int,
            'metric_value_str': self.metric_value_str,
            'date': self.date.isoformat() if self.date else None,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'metadata': self.metadata or {},
            'context': self.context,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
        }

    @classmethod
    def record_metric(cls, session, user_id, metric_name, value, **kwargs):
        """Helper method to record a metric"""
        metric = cls(
            user_id=user_id,
            metric_name=metric_name,
            **kwargs
        )

        # Set value based on type
        if isinstance(value, (int, bool)):
            metric.metric_value_int = int(value)
            metric.metric_value = float(value)
        elif isinstance(value, float):
            metric.metric_value = value
        else:
            metric.metric_value_str = str(value)

        session.add(metric)
        return metric

    def __repr__(self):
        return f'<Analytics {self.metric_name}: {self.metric_value or self.metric_value_int or self.metric_value_str}>'


class ScrapingJob(Base):
    """Model for tracking web scraping jobs"""

    __tablename__ = 'scraping_jobs'

    id = Column(Integer, primary_key=True)

    # Job Information
    job_type = Column(String(100), nullable=False, index=True)  # 'universities', 'professors', 'scholarships'
    status = Column(String(50), default='pending', index=True)  # 'pending', 'running', 'completed', 'failed', 'cancelled'

    # Parameters
    parameters = Column(JSON, default=dict)  # Job configuration
    target_country = Column(String(100), index=True)
    target_domain = Column(String(255))

    # Progress
    progress = Column(Float, default=0.0)  # 0-100 percentage
    items_total = Column(Integer, default=0)
    items_completed = Column(Integer, default=0)
    items_failed = Column(Integer, default=0)

    # Results
    results_count = Column(Integer, default=0)
    new_items_count = Column(Integer, default=0)
    updated_items_count = Column(Integer, default=0)
    skipped_items_count = Column(Integer, default=0)

    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    estimated_completion = Column(DateTime)
    duration_seconds = Column(Integer)

    # Error Handling
    error_message = Column(String(2000))
    error_count = Column(Integer, default=0)
    last_error = Column(DateTime)

    # User
    user_id = Column(Integer, ForeignKey('users.id'), index=True)

    # Metadata
    metadata = Column(JSON, default=dict)
    log = Column(JSON, default=list)  # Job execution log

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert scraping job to dictionary"""
        return {
            'id': self.id,
            'job_type': self.job_type,
            'status': self.status,
            'parameters': self.parameters or {},
            'target_country': self.target_country,
            'progress': self.progress,
            'items_total': self.items_total,
            'items_completed': self.items_completed,
            'items_failed': self.items_failed,
            'results_count': self.results_count,
            'new_items_count': self.new_items_count,
            'updated_items_count': self.updated_items_count,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'estimated_completion': self.estimated_completion.isoformat() if self.estimated_completion else None,
            'duration_seconds': self.duration_seconds,
            'error_message': self.error_message,
            'error_count': self.error_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def update_progress(self, completed, total=None):
        """Update job progress"""
        if total is not None:
            self.items_total = total
        self.items_completed = completed

        if self.items_total > 0:
            self.progress = (self.items_completed / self.items_total) * 100

        # Estimate completion time
        if self.started_at and self.progress > 0 and self.progress < 100:
            elapsed = (datetime.utcnow() - self.started_at).total_seconds()
            total_estimated = (elapsed / self.progress) * 100
            remaining = total_estimated - elapsed
            self.estimated_completion = datetime.utcnow() + timedelta(seconds=remaining)

    def mark_completed(self):
        """Mark job as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        self.progress = 100.0

        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())

    def mark_failed(self, error_message):
        """Mark job as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.error_count += 1
        self.last_error = datetime.utcnow()
        self.completed_at = datetime.utcnow()

        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())

    def add_log(self, message, level='info'):
        """Add log entry to job"""
        if not self.log:
            self.log = []

        self.log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message
        })

    def __repr__(self):
        return f'<ScrapingJob {self.id}: {self.job_type} - {self.status} ({self.progress:.1f}%)>'


from datetime import timedelta
