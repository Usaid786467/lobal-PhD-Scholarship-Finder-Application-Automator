"""
Application Model
Represents a PhD application to a professor
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from . import db


class Application(db.Model):
    """Application model for tracking PhD applications"""

    __tablename__ = 'applications'

    # Status enum values
    STATUS_DRAFT = 'draft'
    STATUS_SENT = 'sent'
    STATUS_DELIVERED = 'delivered'
    STATUS_OPENED = 'opened'
    STATUS_REPLIED = 'replied'
    STATUS_REJECTED = 'rejected'
    STATUS_INTERVIEW = 'interview'
    STATUS_OFFER = 'offer'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DECLINED = 'declined'

    # Primary Key
    id = Column(Integer, primary_key=True)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    professor_id = Column(Integer, ForeignKey('professors.id'), nullable=False, index=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False, index=True)

    # Application Status
    status = Column(String(50), default=STATUS_DRAFT, index=True)
    priority = Column(Integer, default=0)  # 0=normal, 1=high, -1=low

    # Important Dates
    applied_date = Column(DateTime)
    delivered_date = Column(DateTime)
    opened_date = Column(DateTime)
    replied_date = Column(DateTime)
    interview_date = Column(DateTime)
    decision_date = Column(DateTime)

    # Response Information
    response_content = Column(Text)
    response_sentiment = Column(String(50))  # positive, neutral, negative
    response_attachments = Column(JSON)

    # Application Details
    match_score = Column(Float)  # Compatibility score
    match_reasons = Column(JSON)  # Why this professor is a good match
    custom_message = Column(Text)  # Custom part of the email

    # Documents
    documents = Column(JSON)  # List of attached documents
    cv_version = Column(String(200))  # Which CV version was used

    # Follow-up
    follow_up_date = Column(DateTime)
    follow_up_count = Column(Integer, default=0)
    follow_up_sent = Column(Boolean, default=False)

    # Metadata
    notes = Column(Text)
    tags = Column(JSON)  # Custom tags for organization

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    emails = db.relationship('Email', backref='application', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_related=False):
        """Convert application to dictionary"""
        application_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'professor_id': self.professor_id,
            'university_id': self.university_id,
            'status': self.status,
            'priority': self.priority,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'delivered_date': self.delivered_date.isoformat() if self.delivered_date else None,
            'opened_date': self.opened_date.isoformat() if self.opened_date else None,
            'replied_date': self.replied_date.isoformat() if self.replied_date else None,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None,
            'decision_date': self.decision_date.isoformat() if self.decision_date else None,
            'response_content': self.response_content,
            'response_sentiment': self.response_sentiment,
            'response_attachments': self.response_attachments or [],
            'match_score': self.match_score,
            'match_reasons': self.match_reasons or [],
            'custom_message': self.custom_message,
            'documents': self.documents or [],
            'cv_version': self.cv_version,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'follow_up_count': self.follow_up_count,
            'follow_up_sent': self.follow_up_sent,
            'notes': self.notes,
            'tags': self.tags or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_related:
            if self.professor:
                application_dict['professor'] = self.professor.to_dict()
            if self.university:
                application_dict['university'] = self.university.to_dict()
            application_dict['emails'] = [email.to_dict() for email in self.emails.all()]

        return application_dict

    def update_status(self, new_status, commit=True):
        """Update application status and set appropriate timestamps"""
        self.status = new_status
        now = datetime.utcnow()

        if new_status == self.STATUS_SENT:
            self.applied_date = now
        elif new_status == self.STATUS_DELIVERED:
            self.delivered_date = now
        elif new_status == self.STATUS_OPENED:
            self.opened_date = now
        elif new_status == self.STATUS_REPLIED:
            self.replied_date = now

        if commit:
            db.session.commit()

    def __repr__(self):
        return f'<Application {self.id} - {self.status}>'
