"""
Analytics model for tracking metrics and statistics
"""
from datetime import datetime
from models.database import db
import json


class Analytics(db.Model):
    """Analytics model for storing application metrics"""

    __tablename__ = 'analytics'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Metric Information
    metric_name = db.Column(db.String(100), nullable=False, index=True)
    metric_value = db.Column(db.Float, nullable=False)

    # Date
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False, index=True)

    # Additional metadata (stored as JSON)
    metadata = db.Column(db.Text, nullable=True)  # JSON object

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Metric name constants
    METRIC_APPLICATIONS_SENT = 'applications_sent'
    METRIC_RESPONSES_RECEIVED = 'responses_received'
    METRIC_ACCEPTANCE_RATE = 'acceptance_rate'
    METRIC_RESPONSE_RATE = 'response_rate'
    METRIC_AVERAGE_RESPONSE_TIME = 'average_response_time'
    METRIC_EMAILS_SENT = 'emails_sent'
    METRIC_EMAILS_OPENED = 'emails_opened'
    METRIC_OPEN_RATE = 'open_rate'
    METRIC_UNIVERSITIES_DISCOVERED = 'universities_discovered'
    METRIC_PROFESSORS_FOUND = 'professors_found'

    def __init__(self, user_id, metric_name, metric_value, **kwargs):
        """Initialize analytics entry"""
        self.user_id = user_id
        self.metric_name = metric_name
        self.metric_value = metric_value
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_metadata(self, metadata):
        """Set metadata from dictionary"""
        if isinstance(metadata, dict):
            self.metadata = json.dumps(metadata)
        elif isinstance(metadata, str):
            self.metadata = metadata

    def get_metadata(self):
        """Get metadata as dictionary"""
        if self.metadata:
            try:
                return json.loads(self.metadata)
            except:
                return {}
        return {}

    def to_dict(self):
        """Convert analytics to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'date': self.date.isoformat() if self.date else None,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        """String representation"""
        return f'<Analytics {self.metric_name}: {self.metric_value}>'


class ScrapingJob(db.Model):
    """Scraping job model for tracking web scraping tasks"""

    __tablename__ = 'scraping_jobs'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Job Type
    # Possible types: universities, professors, scholarships, publications
    job_type = db.Column(db.String(50), nullable=False, index=True)

    # Status
    # Possible statuses: pending, running, completed, failed, cancelled
    status = db.Column(
        db.String(50),
        default='pending',
        nullable=False,
        index=True
    )

    # Job Parameters (stored as JSON)
    parameters = db.Column(db.Text, nullable=True)  # JSON object

    # Progress
    progress = db.Column(db.Integer, default=0, nullable=False)  # 0-100
    results_count = db.Column(db.Integer, default=0, nullable=False)

    # Timestamps
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Error Information
    error_message = db.Column(db.Text, nullable=True)

    # Job Type constants
    JOB_TYPE_UNIVERSITIES = 'universities'
    JOB_TYPE_PROFESSORS = 'professors'
    JOB_TYPE_SCHOLARSHIPS = 'scholarships'
    JOB_TYPE_PUBLICATIONS = 'publications'

    VALID_JOB_TYPES = [
        JOB_TYPE_UNIVERSITIES,
        JOB_TYPE_PROFESSORS,
        JOB_TYPE_SCHOLARSHIPS,
        JOB_TYPE_PUBLICATIONS
    ]

    # Status constants
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'

    VALID_STATUSES = [
        STATUS_PENDING,
        STATUS_RUNNING,
        STATUS_COMPLETED,
        STATUS_FAILED,
        STATUS_CANCELLED
    ]

    def __init__(self, job_type, **kwargs):
        """Initialize scraping job"""
        if job_type not in self.VALID_JOB_TYPES:
            raise ValueError(f"Invalid job type: {job_type}")

        self.job_type = job_type
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_parameters(self, parameters):
        """Set job parameters from dictionary"""
        if isinstance(parameters, dict):
            self.parameters = json.dumps(parameters)
        elif isinstance(parameters, str):
            self.parameters = parameters

    def get_parameters(self):
        """Get job parameters as dictionary"""
        if self.parameters:
            try:
                return json.loads(self.parameters)
            except:
                return {}
        return {}

    def update_status(self, new_status):
        """Update job status"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")

        old_status = self.status
        self.status = new_status

        # Update timestamps
        if new_status == self.STATUS_RUNNING and not self.started_at:
            self.started_at = datetime.utcnow()
        elif new_status in [self.STATUS_COMPLETED, self.STATUS_FAILED, self.STATUS_CANCELLED]:
            if not self.completed_at:
                self.completed_at = datetime.utcnow()
            if new_status == self.STATUS_COMPLETED:
                self.progress = 100

    def update_progress(self, progress):
        """Update job progress (0-100)"""
        self.progress = max(0, min(100, progress))

    def increment_results(self, count=1):
        """Increment results count"""
        self.results_count += count

    def mark_as_failed(self, error_message):
        """Mark job as failed"""
        self.update_status(self.STATUS_FAILED)
        self.error_message = error_message

    def mark_as_completed(self):
        """Mark job as completed"""
        self.update_status(self.STATUS_COMPLETED)
        self.progress = 100

    def get_duration(self):
        """Get job duration in seconds"""
        if self.started_at:
            end_time = self.completed_at or datetime.utcnow()
            return (end_time - self.started_at).total_seconds()
        return 0

    def to_dict(self):
        """Convert scraping job to dictionary"""
        return {
            'id': self.id,
            'job_type': self.job_type,
            'status': self.status,
            'parameters': self.get_parameters(),
            'progress': self.progress,
            'results_count': self.results_count,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'error_message': self.error_message,
            'duration_seconds': self.get_duration()
        }

    def __repr__(self):
        """String representation"""
        return f'<ScrapingJob {self.id}: {self.job_type} - {self.status}>'
