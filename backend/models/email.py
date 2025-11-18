"""
Email models for managing email communications
"""
from datetime import datetime
from models.database import db


class Email(db.Model):
    """Email model for tracking individual emails"""

    __tablename__ = 'emails'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False, index=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('email_batches.id'), nullable=True, index=True)

    # Email Content
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    template_id = db.Column(db.Integer, nullable=True)  # Reference to template used

    # Status
    # Possible statuses: draft, pending, approved, scheduled, sending, sent, failed, bounced
    status = db.Column(
        db.String(50),
        default='draft',
        nullable=False,
        index=True
    )

    # Scheduling
    scheduled_time = db.Column(db.DateTime, nullable=True)

    # Timestamps
    sent_at = db.Column(db.DateTime, nullable=True, index=True)
    opened_at = db.Column(db.DateTime, nullable=True)
    replied_at = db.Column(db.DateTime, nullable=True)

    # Error Handling
    error_message = db.Column(db.Text, nullable=True)
    retry_count = db.Column(db.Integer, default=0, nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Status options
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_SENDING = 'sending'
    STATUS_SENT = 'sent'
    STATUS_FAILED = 'failed'
    STATUS_BOUNCED = 'bounced'

    VALID_STATUSES = [
        STATUS_DRAFT, STATUS_PENDING, STATUS_APPROVED, STATUS_SCHEDULED,
        STATUS_SENDING, STATUS_SENT, STATUS_FAILED, STATUS_BOUNCED
    ]

    def __init__(self, application_id, subject, body, **kwargs):
        """Initialize email with required fields"""
        self.application_id = application_id
        self.subject = subject
        self.body = body
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def update_status(self, new_status):
        """Update email status"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")

        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()

        # Update timestamps based on status
        if new_status == self.STATUS_SENT and not self.sent_at:
            self.sent_at = datetime.utcnow()
        elif new_status == self.STATUS_FAILED:
            self.retry_count += 1

    def mark_as_sent(self):
        """Mark email as sent"""
        self.update_status(self.STATUS_SENT)
        self.sent_at = datetime.utcnow()

        # Update application status
        if self.application:
            self.application.mark_as_sent()

    def mark_as_opened(self):
        """Mark email as opened"""
        if not self.opened_at:
            self.opened_at = datetime.utcnow()

        # Update application status
        if self.application and self.application.status != 'replied':
            self.application.mark_as_opened()

    def mark_as_replied(self):
        """Mark email as replied"""
        if not self.replied_at:
            self.replied_at = datetime.utcnow()

        # Update application status
        if self.application:
            self.application.mark_as_replied()

    def mark_as_failed(self, error_message):
        """Mark email as failed"""
        self.update_status(self.STATUS_FAILED)
        self.error_message = error_message

    def approve(self):
        """Approve email for sending"""
        self.update_status(self.STATUS_APPROVED)

    def schedule(self, scheduled_time):
        """Schedule email for future sending"""
        self.scheduled_time = scheduled_time
        self.update_status(self.STATUS_SCHEDULED)

    def can_retry(self, max_retries=3):
        """Check if email can be retried"""
        return self.status == self.STATUS_FAILED and self.retry_count < max_retries

    def to_dict(self, include_application=False):
        """Convert email to dictionary"""
        data = {
            'id': self.id,
            'application_id': self.application_id,
            'batch_id': self.batch_id,
            'subject': self.subject,
            'body': self.body,
            'template_id': self.template_id,
            'status': self.status,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if include_application and self.application:
            data['application'] = self.application.to_dict(include_related=True)

        return data

    def __repr__(self):
        """String representation"""
        return f'<Email {self.id}: {self.status}>'


class EmailBatch(db.Model):
    """Email batch model for managing batch operations"""

    __tablename__ = 'email_batches'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Batch Information
    name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Counts
    total_count = db.Column(db.Integer, default=0, nullable=False)
    approved_count = db.Column(db.Integer, default=0, nullable=False)
    sent_count = db.Column(db.Integer, default=0, nullable=False)
    failed_count = db.Column(db.Integer, default=0, nullable=False)

    # Status
    # Possible statuses: draft, pending_approval, approved, sending, completed, failed
    status = db.Column(
        db.String(50),
        default='draft',
        nullable=False,
        index=True
    )

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    approved_at = db.Column(db.DateTime, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    emails = db.relationship('Email', backref='batch', lazy='dynamic')

    # Status options
    STATUS_DRAFT = 'draft'
    STATUS_PENDING_APPROVAL = 'pending_approval'
    STATUS_APPROVED = 'approved'
    STATUS_SENDING = 'sending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    VALID_STATUSES = [
        STATUS_DRAFT, STATUS_PENDING_APPROVAL, STATUS_APPROVED,
        STATUS_SENDING, STATUS_COMPLETED, STATUS_FAILED
    ]

    def __init__(self, user_id, name=None, **kwargs):
        """Initialize batch with required fields"""
        self.user_id = user_id
        self.name = name or f"Batch {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def update_status(self, new_status):
        """Update batch status"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")

        self.status = new_status

        # Update timestamps
        if new_status == self.STATUS_APPROVED and not self.approved_at:
            self.approved_at = datetime.utcnow()
        elif new_status == self.STATUS_SENDING and not self.started_at:
            self.started_at = datetime.utcnow()
        elif new_status in [self.STATUS_COMPLETED, self.STATUS_FAILED] and not self.completed_at:
            self.completed_at = datetime.utcnow()

    def update_counts(self):
        """Update email counts"""
        self.total_count = self.emails.count()
        self.approved_count = self.emails.filter_by(status=Email.STATUS_APPROVED).count()
        self.sent_count = self.emails.filter_by(status=Email.STATUS_SENT).count()
        self.failed_count = self.emails.filter_by(status=Email.STATUS_FAILED).count()

    def approve_all(self):
        """Approve all emails in batch"""
        for email in self.emails.filter_by(status=Email.STATUS_PENDING).all():
            email.approve()
        self.update_counts()
        self.update_status(self.STATUS_APPROVED)

    def get_progress_percentage(self):
        """Get sending progress as percentage"""
        if self.total_count == 0:
            return 0
        return int((self.sent_count / self.total_count) * 100)

    def to_dict(self, include_emails=False):
        """Convert batch to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'total_count': self.total_count,
            'approved_count': self.approved_count,
            'sent_count': self.sent_count,
            'failed_count': self.failed_count,
            'status': self.status,
            'progress_percentage': self.get_progress_percentage(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

        if include_emails:
            data['emails'] = [email.to_dict() for email in self.emails.all()]

        return data

    def __repr__(self):
        """String representation"""
        return f'<EmailBatch {self.id}: {self.name}>'
