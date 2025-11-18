"""
Application Model for PhD Application Automator
Tracks PhD application progress and status
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class ApplicationStatus(enum.Enum):
    """Application status enumeration"""
    DRAFT = 'draft'
    SENT = 'sent'
    DELIVERED = 'delivered'
    OPENED = 'opened'
    REPLIED = 'replied'
    INTERVIEW_REQUESTED = 'interview_requested'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'


class Application(Base):
    """Application model for tracking PhD applications"""

    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)

    # Relationships
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    professor_id = Column(Integer, ForeignKey('professors.id'), nullable=False, index=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False, index=True)

    # Status
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT, nullable=False, index=True)
    status_history = Column(JSON, default=list)  # Track status changes with timestamps

    # Dates
    applied_date = Column(DateTime)  # When email was sent
    delivered_date = Column(DateTime)  # Email delivered
    opened_date = Column(DateTime)  # Professor opened email
    replied_date = Column(DateTime)  # Professor replied
    last_contact_date = Column(DateTime)  # Last interaction
    deadline_date = Column(DateTime)  # Application deadline

    # Communication
    email_subject = Column(String(500))
    email_sent = Column(Integer, default=0)  # Number of emails sent
    email_opened = Column(Integer, default=0)  # Number of times email was opened
    follow_up_count = Column(Integer, default=0)
    next_follow_up_date = Column(DateTime)

    # Response
    response_received = Column(Integer, default=False)
    response_content = Column(Text)  # Content of professor's response
    response_sentiment = Column(String(50))  # 'positive', 'negative', 'neutral'

    # Documents
    documents = Column(JSON, default=list)  # List of attached documents
    cv_version = Column(String(255))  # Which CV version was sent
    cover_letter_path = Column(String(500))
    research_proposal_path = Column(String(500))

    # Match Information
    match_score = Column(Integer)  # Match score at time of application
    match_reasons = Column(JSON, default=list)

    # User Notes
    notes = Column(Text)  # Personal notes about this application
    tags = Column(JSON, default=list)  # Custom tags for organization

    # Reminders
    reminder_date = Column(DateTime)
    reminder_message = Column(String(500))

    # Interview Information
    interview_scheduled = Column(Integer, default=False)
    interview_date = Column(DateTime)
    interview_type = Column(String(100))  # 'video', 'phone', 'in-person'
    interview_notes = Column(Text)

    # Decision
    decision = Column(String(50))  # 'accepted', 'rejected', 'waitlisted'
    decision_date = Column(DateTime)
    decision_notes = Column(Text)

    # Funding
    funding_offered = Column(Integer, default=False)
    funding_amount = Column(String(255))
    funding_duration = Column(String(100))

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_details=True):
        """Convert application to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'professor_id': self.professor_id,
            'university_id': self.university_id,
            'status': self.status.value if self.status else None,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'last_contact_date': self.last_contact_date.isoformat() if self.last_contact_date else None,
            'deadline_date': self.deadline_date.isoformat() if self.deadline_date else None,
            'response_received': bool(self.response_received),
            'match_score': self.match_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_details:
            data.update({
                'status_history': self.status_history or [],
                'delivered_date': self.delivered_date.isoformat() if self.delivered_date else None,
                'opened_date': self.opened_date.isoformat() if self.opened_date else None,
                'replied_date': self.replied_date.isoformat() if self.replied_date else None,
                'email_subject': self.email_subject,
                'email_sent': self.email_sent,
                'email_opened': self.email_opened,
                'follow_up_count': self.follow_up_count,
                'next_follow_up_date': self.next_follow_up_date.isoformat() if self.next_follow_up_date else None,
                'response_content': self.response_content,
                'response_sentiment': self.response_sentiment,
                'documents': self.documents or [],
                'cv_version': self.cv_version,
                'match_reasons': self.match_reasons or [],
                'notes': self.notes,
                'tags': self.tags or [],
                'reminder_date': self.reminder_date.isoformat() if self.reminder_date else None,
                'reminder_message': self.reminder_message,
                'interview_scheduled': bool(self.interview_scheduled),
                'interview_date': self.interview_date.isoformat() if self.interview_date else None,
                'interview_type': self.interview_type,
                'interview_notes': self.interview_notes,
                'decision': self.decision,
                'decision_date': self.decision_date.isoformat() if self.decision_date else None,
                'decision_notes': self.decision_notes,
                'funding_offered': bool(self.funding_offered),
                'funding_amount': self.funding_amount,
                'funding_duration': self.funding_duration,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            })

        return data

    def update_status(self, new_status, notes=None):
        """Update application status and track history"""
        old_status = self.status.value if self.status else None

        # Update status
        if isinstance(new_status, str):
            self.status = ApplicationStatus(new_status)
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

        # Update relevant dates
        now = datetime.utcnow()
        if self.status == ApplicationStatus.SENT:
            self.applied_date = now
        elif self.status == ApplicationStatus.OPENED:
            self.opened_date = now
        elif self.status == ApplicationStatus.REPLIED:
            self.replied_date = now
            self.response_received = True

        self.last_contact_date = now

    def record_email_sent(self):
        """Record that an email was sent"""
        self.email_sent += 1
        self.last_contact_date = datetime.utcnow()
        if not self.applied_date:
            self.applied_date = datetime.utcnow()

    def record_email_opened(self):
        """Record that email was opened"""
        self.email_opened += 1
        if not self.opened_date:
            self.opened_date = datetime.utcnow()
        if self.status == ApplicationStatus.SENT or self.status == ApplicationStatus.DELIVERED:
            self.update_status(ApplicationStatus.OPENED)

    def __repr__(self):
        return f'<Application {self.id} - Status: {self.status.value if self.status else "unknown"}>'
