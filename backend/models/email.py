"""
Email Models
Manages email drafts, batches, and sending
"""
from datetime import datetime
from models import db


class EmailBatch(db.Model):
    """Email batch for managing bulk email operations"""

    __tablename__ = 'email_batches'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    total_count = db.Column(db.Integer, default=0)
    sent_count = db.Column(db.Integer, default=0)

    status = db.Column(db.String(50), default='draft', index=True)
    # Statuses: draft, approved, sending, completed, failed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    emails = db.relationship('Email', backref='batch', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self) -> dict:
        """Convert batch to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_count': self.total_count,
            'sent_count': self.sent_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f'<EmailBatch {self.id} - {self.sent_count}/{self.total_count}>'


class Email(db.Model):
    """Email model for storing draft and sent emails"""

    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False, index=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('email_batches.id'), index=True)

    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(50), default='draft', index=True)
    # Statuses: draft, approved, scheduled, sent, delivered, opened, bounced, failed

    scheduled_time = db.Column(db.DateTime)
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    opened_at = db.Column(db.DateTime)

    # Error tracking
    error_message = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert email to dictionary"""
        return {
            'id': self.id,
            'application_id': self.application_id,
            'batch_id': self.batch_id,
            'subject': self.subject,
            'body': self.body,
            'status': self.status,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f'<Email {self.id} - {self.status}>'
