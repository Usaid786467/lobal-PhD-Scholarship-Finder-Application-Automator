"""
Email Models
Represents emails and email batches
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from . import db


class Email(db.Model):
    """Email model for tracking individual emails"""

    __tablename__ = 'emails'

    # Status enum values
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_SENDING = 'sending'
    STATUS_SENT = 'sent'
    STATUS_FAILED = 'failed'
    STATUS_BOUNCED = 'bounced'

    # Primary Key
    id = Column(Integer, primary_key=True)

    # Foreign Keys
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False, index=True)
    batch_id = Column(Integer, ForeignKey('email_batches.id'), index=True)

    # Email Content
    to_email = Column(String(255), nullable=False)
    to_name = Column(String(255))
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    html_body = Column(Text)  # HTML version of the email

    # Template Information
    template_id = Column(String(100))
    template_variables = Column(JSON)  # Variables used in the template

    # Attachments
    attachments = Column(JSON)  # List of file paths to attach

    # Email Status
    status = Column(String(50), default=STATUS_DRAFT, index=True)
    priority = Column(Integer, default=0)

    # Scheduling
    scheduled_time = Column(DateTime, index=True)

    # Sending Information
    sent_at = Column(DateTime, index=True)
    delivered_at = Column(DateTime)
    opened_at = Column(DateTime)
    clicked_at = Column(DateTime)
    replied_at = Column(DateTime)

    # Tracking
    tracking_id = Column(String(255), unique=True)  # For open/click tracking
    opened_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)

    # Error Handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    # Email Provider Information
    provider = Column(String(50))  # smtp, sendgrid, mailgun
    provider_message_id = Column(String(255))  # Provider's message ID

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_body=True):
        """Convert email to dictionary"""
        email_dict = {
            'id': self.id,
            'application_id': self.application_id,
            'batch_id': self.batch_id,
            'to_email': self.to_email,
            'to_name': self.to_name,
            'subject': self.subject,
            'template_id': self.template_id,
            'status': self.status,
            'priority': self.priority,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'clicked_at': self.clicked_at.isoformat() if self.clicked_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
            'opened_count': self.opened_count,
            'clicked_count': self.clicked_count,
            'retry_count': self.retry_count,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_body:
            email_dict['body'] = self.body
            email_dict['html_body'] = self.html_body
            email_dict['attachments'] = self.attachments or []

        return email_dict

    def __repr__(self):
        return f'<Email {self.id} to {self.to_email} - {self.status}>'


class EmailBatch(db.Model):
    """EmailBatch model for managing batch email operations"""

    __tablename__ = 'email_batches'

    # Status enum values
    STATUS_DRAFT = 'draft'
    STATUS_PENDING_APPROVAL = 'pending_approval'
    STATUS_APPROVED = 'approved'
    STATUS_SENDING = 'sending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'

    # Primary Key
    id = Column(Integer, primary_key=True)

    # Foreign Key
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Batch Information
    name = Column(String(255))
    description = Column(Text)

    # Statistics
    total_count = Column(Integer, default=0)
    approved_count = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    bounced_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    replied_count = Column(Integer, default=0)

    # Status
    status = Column(String(50), default=STATUS_DRAFT, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    cancelled_at = Column(DateTime)

    # Relationships
    emails = db.relationship('Email', backref='batch', lazy='dynamic')

    def to_dict(self, include_emails=False):
        """Convert batch to dictionary"""
        batch_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'total_count': self.total_count,
            'approved_count': self.approved_count,
            'sent_count': self.sent_count,
            'failed_count': self.failed_count,
            'bounced_count': self.bounced_count,
            'opened_count': self.opened_count,
            'replied_count': self.replied_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'progress_percentage': self.get_progress_percentage(),
        }

        if include_emails:
            batch_dict['emails'] = [email.to_dict() for email in self.emails.all()]

        return batch_dict

    def get_progress_percentage(self):
        """Calculate progress percentage"""
        if self.total_count == 0:
            return 0
        return round((self.sent_count / self.total_count) * 100, 2)

    def update_counts(self):
        """Update email counts from related emails"""
        self.total_count = self.emails.count()
        self.approved_count = self.emails.filter_by(status=Email.STATUS_APPROVED).count()
        self.sent_count = self.emails.filter(
            Email.status.in_([Email.STATUS_SENT, Email.STATUS_DELIVERED])
        ).count()
        self.failed_count = self.emails.filter_by(status=Email.STATUS_FAILED).count()
        self.bounced_count = self.emails.filter_by(status=Email.STATUS_BOUNCED).count()
        self.opened_count = self.emails.filter(Email.opened_at.isnot(None)).count()
        self.replied_count = self.emails.filter(Email.replied_at.isnot(None)).count()
        db.session.commit()

    def __repr__(self):
        return f'<EmailBatch {self.id} - {self.name}>'
