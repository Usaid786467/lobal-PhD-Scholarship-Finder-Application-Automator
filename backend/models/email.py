"""
Email Models for PhD Application Automator
Handles email drafts, batches, and sending management
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class EmailStatus(enum.Enum):
    """Email status enumeration"""
    DRAFT = 'draft'
    PENDING_APPROVAL = 'pending_approval'
    APPROVED = 'approved'
    SCHEDULED = 'scheduled'
    SENDING = 'sending'
    SENT = 'sent'
    DELIVERED = 'delivered'
    OPENED = 'opened'
    REPLIED = 'replied'
    FAILED = 'failed'
    BOUNCED = 'bounced'
    REJECTED = 'rejected'


class Email(Base):
    """Email model for managing email communications"""

    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)

    # Relationships
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    professor_id = Column(Integer, ForeignKey('professors.id'), nullable=False, index=True)
    batch_id = Column(Integer, ForeignKey('email_batches.id'), index=True)

    # Email Content
    recipient_email = Column(String(255), nullable=False, index=True)
    recipient_name = Column(String(255))
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)  # HTML or plain text
    body_format = Column(String(20), default='html')  # 'html' or 'plain'

    # Template Information
    template_id = Column(Integer)
    template_name = Column(String(255))
    template_variables = Column(JSON, default=dict)  # Variables used in template

    # Attachments
    attachments = Column(JSON, default=list)  # List of attachment file paths
    cv_attached = Column(Boolean, default=False)
    cv_path = Column(String(500))

    # Status
    status = Column(Enum(EmailStatus), default=EmailStatus.DRAFT, nullable=False, index=True)
    status_history = Column(JSON, default=list)  # Track status changes

    # Scheduling
    scheduled_time = Column(DateTime, index=True)
    send_after = Column(DateTime)  # Don't send before this time
    send_before = Column(DateTime)  # Must send before this time

    # Sending Information
    sent_at = Column(DateTime, index=True)
    delivered_at = Column(DateTime)
    opened_at = Column(DateTime)
    replied_at = Column(DateTime)
    last_opened_at = Column(DateTime)
    open_count = Column(Integer, default=0)

    # Response Tracking
    reply_content = Column(Text)
    reply_received_at = Column(DateTime)
    reply_sentiment = Column(String(50))  # 'positive', 'negative', 'neutral'

    # Sending Metadata
    message_id = Column(String(500))  # Provider's message ID
    smtp_response = Column(Text)  # SMTP server response
    provider = Column(String(100))  # 'gmail', 'sendgrid', 'mailgun'
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    # Error Handling
    error_message = Column(Text)
    error_code = Column(String(100))
    bounce_reason = Column(String(500))
    last_error = Column(DateTime)

    # Analytics
    unique_opens = Column(Integer, default=0)
    unique_clicks = Column(Integer, default=0)
    click_data = Column(JSON, default=list)  # Track link clicks

    # Priority
    priority = Column(Integer, default=5)  # 1-10, higher = more important
    is_follow_up = Column(Boolean, default=False)
    follow_up_number = Column(Integer, default=0)  # 1st follow-up, 2nd, etc.

    # Approval
    requires_approval = Column(Boolean, default=True)
    approved_by = Column(Integer, ForeignKey('users.id'))
    approved_at = Column(DateTime)

    # Notes
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_body=True):
        """Convert email to dictionary"""
        data = {
            'id': self.id,
            'application_id': self.application_id,
            'user_id': self.user_id,
            'professor_id': self.professor_id,
            'batch_id': self.batch_id,
            'recipient_email': self.recipient_email,
            'recipient_name': self.recipient_name,
            'subject': self.subject,
            'status': self.status.value if self.status else None,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
            'open_count': self.open_count,
            'is_follow_up': self.is_follow_up,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_body:
            data.update({
                'body': self.body,
                'body_format': self.body_format,
                'template_name': self.template_name,
                'template_variables': self.template_variables or {},
                'attachments': self.attachments or [],
                'cv_attached': self.cv_attached,
                'status_history': self.status_history or [],
                'error_message': self.error_message,
                'retry_count': self.retry_count,
                'reply_content': self.reply_content,
                'reply_sentiment': self.reply_sentiment,
                'priority': self.priority,
                'notes': self.notes,
            })

        return data

    def update_status(self, new_status, notes=None):
        """Update email status and track history"""
        old_status = self.status.value if self.status else None

        # Update status
        if isinstance(new_status, str):
            self.status = EmailStatus(new_status)
        else:
            self.status = new_status

        # Add to history
        if not self.status_history:
            self.status_history = []

        self.status_history.append({
            'from_status': old_status,
            'to_status': self.status.value,
            'timestamp': datetime.utcnow().isoformat(),
            'notes': notes
        })

        # Update relevant timestamps
        now = datetime.utcnow()
        if self.status == EmailStatus.SENT:
            self.sent_at = now
        elif self.status == EmailStatus.DELIVERED:
            self.delivered_at = now
        elif self.status == EmailStatus.OPENED:
            if not self.opened_at:
                self.opened_at = now
            self.last_opened_at = now
            self.open_count += 1
        elif self.status == EmailStatus.REPLIED:
            self.replied_at = now

    def approve(self, user_id):
        """Approve email for sending"""
        self.approved_by = user_id
        self.approved_at = datetime.utcnow()
        self.update_status(EmailStatus.APPROVED, 'Email approved for sending')

    def schedule(self, send_time):
        """Schedule email for sending"""
        self.scheduled_time = send_time
        self.update_status(EmailStatus.SCHEDULED, f'Scheduled for {send_time}')

    def mark_failed(self, error_message, error_code=None):
        """Mark email as failed"""
        self.error_message = error_message
        self.error_code = error_code
        self.last_error = datetime.utcnow()
        self.retry_count += 1
        self.update_status(EmailStatus.FAILED, f'Failed: {error_message}')

    def __repr__(self):
        return f'<Email {self.id} to {self.recipient_email} - Status: {self.status.value if self.status else "unknown"}>'


class EmailBatch(Base):
    """Email batch model for managing bulk email operations"""

    __tablename__ = 'email_batches'

    id = Column(Integer, primary_key=True)

    # Batch Information
    name = Column(String(255), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Statistics
    total_count = Column(Integer, default=0)
    draft_count = Column(Integer, default=0)
    approved_count = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    replied_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    # Status
    status = Column(String(50), default='draft', index=True)  # 'draft', 'pending_approval', 'approved', 'sending', 'completed', 'cancelled'

    # Scheduling
    scheduled_start = Column(DateTime)
    scheduled_end = Column(DateTime)

    # Execution
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    cancelled_at = Column(DateTime)

    # Settings
    send_rate = Column(Integer, default=50)  # Emails per hour
    max_daily = Column(Integer, default=1000)  # Max emails per day

    # Approval
    requires_approval = Column(Boolean, default=True)
    approved_by = Column(Integer, ForeignKey('users.id'))
    approved_at = Column(DateTime)

    # Notes
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert batch to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'total_count': self.total_count,
            'draft_count': self.draft_count,
            'approved_count': self.approved_count,
            'sent_count': self.sent_count,
            'delivered_count': self.delivered_count,
            'opened_count': self.opened_count,
            'replied_count': self.replied_count,
            'failed_count': self.failed_count,
            'status': self.status,
            'scheduled_start': self.scheduled_start.isoformat() if self.scheduled_start else None,
            'scheduled_end': self.scheduled_end.isoformat() if self.scheduled_end else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'send_rate': self.send_rate,
            'max_daily': self.max_daily,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def update_counts(self, session):
        """Update email counts from associated emails"""
        from sqlalchemy import func

        # Get counts by status
        counts = session.query(
            Email.status,
            func.count(Email.id)
        ).filter(
            Email.batch_id == self.id
        ).group_by(Email.status).all()

        # Reset counts
        self.total_count = 0
        self.draft_count = 0
        self.approved_count = 0
        self.sent_count = 0
        self.delivered_count = 0
        self.opened_count = 0
        self.replied_count = 0
        self.failed_count = 0

        # Update counts
        for status, count in counts:
            self.total_count += count
            if status == EmailStatus.DRAFT:
                self.draft_count = count
            elif status == EmailStatus.APPROVED:
                self.approved_count = count
            elif status == EmailStatus.SENT:
                self.sent_count = count
            elif status == EmailStatus.DELIVERED:
                self.delivered_count = count
            elif status == EmailStatus.OPENED:
                self.opened_count = count
            elif status == EmailStatus.REPLIED:
                self.replied_count = count
            elif status == EmailStatus.FAILED or status == EmailStatus.BOUNCED:
                self.failed_count += count

    def __repr__(self):
        return f'<EmailBatch {self.id}: {self.name} ({self.total_count} emails)>'
