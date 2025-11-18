"""
Application model for tracking PhD applications
"""
from datetime import datetime
from models.database import db
import json


class Application(db.Model):
    """Application model for tracking application status"""

    __tablename__ = 'applications'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'), nullable=False, index=True)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False, index=True)

    # Status tracking
    # Possible statuses: draft, sent, delivered, opened, replied, accepted, rejected, withdrawn
    status = db.Column(
        db.String(50),
        default='draft',
        nullable=False,
        index=True
    )

    # Dates
    applied_date = db.Column(db.DateTime, nullable=True)
    opened_date = db.Column(db.DateTime, nullable=True)
    replied_date = db.Column(db.DateTime, nullable=True)

    # Response Information
    response_content = db.Column(db.Text, nullable=True)

    # Notes and Documentation
    notes = db.Column(db.Text, nullable=True)
    documents = db.Column(db.Text, nullable=True)  # JSON array of document paths

    # Follow-up
    follow_up_date = db.Column(db.DateTime, nullable=True)
    follow_up_sent = db.Column(db.Boolean, default=False, nullable=False)

    # Match Score
    match_score = db.Column(db.Integer, nullable=True)  # 0-100

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    emails = db.relationship('Email', backref='application', lazy='dynamic', cascade='all, delete-orphan')

    # Status options
    STATUS_DRAFT = 'draft'
    STATUS_SENT = 'sent'
    STATUS_DELIVERED = 'delivered'
    STATUS_OPENED = 'opened'
    STATUS_REPLIED = 'replied'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_WITHDRAWN = 'withdrawn'

    VALID_STATUSES = [
        STATUS_DRAFT, STATUS_SENT, STATUS_DELIVERED, STATUS_OPENED,
        STATUS_REPLIED, STATUS_ACCEPTED, STATUS_REJECTED, STATUS_WITHDRAWN
    ]

    def __init__(self, user_id, professor_id, university_id, **kwargs):
        """Initialize application with required fields"""
        self.user_id = user_id
        self.professor_id = professor_id
        self.university_id = university_id
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_documents(self, documents):
        """Set documents from list"""
        if isinstance(documents, list):
            self.documents = json.dumps(documents)
        elif isinstance(documents, str):
            self.documents = documents

    def get_documents(self):
        """Get documents as list"""
        if self.documents:
            try:
                return json.loads(self.documents)
            except:
                return []
        return []

    def add_document(self, document_path):
        """Add a document to the list"""
        docs = self.get_documents()
        docs.append(document_path)
        self.set_documents(docs)

    def update_status(self, new_status):
        """Update application status"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")

        self.status = new_status
        self.updated_at = datetime.utcnow()

        # Update relevant dates
        if new_status == self.STATUS_SENT and not self.applied_date:
            self.applied_date = datetime.utcnow()
        elif new_status == self.STATUS_OPENED and not self.opened_date:
            self.opened_date = datetime.utcnow()
        elif new_status == self.STATUS_REPLIED and not self.replied_date:
            self.replied_date = datetime.utcnow()

    def add_note(self, note):
        """Add a note to existing notes"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        new_note = f"[{timestamp}] {note}"

        if self.notes:
            self.notes += f"\n{new_note}"
        else:
            self.notes = new_note

    def mark_as_sent(self):
        """Mark application as sent"""
        self.update_status(self.STATUS_SENT)
        self.applied_date = datetime.utcnow()

    def mark_as_opened(self):
        """Mark application as opened"""
        self.update_status(self.STATUS_OPENED)
        self.opened_date = datetime.utcnow()

    def mark_as_replied(self):
        """Mark application as replied"""
        self.update_status(self.STATUS_REPLIED)
        self.replied_date = datetime.utcnow()

    def schedule_follow_up(self, days=14):
        """Schedule a follow-up after specified days"""
        from datetime import timedelta
        self.follow_up_date = datetime.utcnow() + timedelta(days=days)

    def to_dict(self, include_related=False):
        """Convert application to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'professor_id': self.professor_id,
            'university_id': self.university_id,
            'status': self.status,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'opened_date': self.opened_date.isoformat() if self.opened_date else None,
            'replied_date': self.replied_date.isoformat() if self.replied_date else None,
            'response_content': self.response_content,
            'notes': self.notes,
            'documents': self.get_documents(),
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'follow_up_sent': self.follow_up_sent,
            'match_score': self.match_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'email_count': self.emails.count()
        }

        if include_related:
            if self.professor:
                data['professor'] = self.professor.to_dict()
            if self.university:
                data['university'] = self.university.to_dict()

        return data

    def __repr__(self):
        """String representation"""
        return f'<Application {self.id}: {self.status}>'
