"""
Application Model
Tracks PhD applications to professors
"""
from datetime import datetime
from models import db


class Application(db.Model):
    """Application model for tracking PhD applications"""

    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'), nullable=False, index=True)

    # Application status
    status = db.Column(db.String(50), default='draft', index=True)
    # Statuses: draft, approved, sent, delivered, opened, replied, rejected

    # Match score (0-100)
    match_score = db.Column(db.Float, default=0.0)

    # Dates
    applied_date = db.Column(db.DateTime)
    opened_date = db.Column(db.DateTime)
    replied_date = db.Column(db.DateTime)

    # Notes
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    emails = db.relationship('Email', backref='application', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self) -> dict:
        """Convert application to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'professor_id': self.professor_id,
            'professor_name': self.professor.name if self.professor else None,
            'professor_email': self.professor.email if self.professor else None,
            'university_name': self.professor.university.name if self.professor and self.professor.university else None,
            'status': self.status,
            'match_score': self.match_score,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'opened_date': self.opened_date.isoformat() if self.opened_date else None,
            'replied_date': self.replied_date.isoformat() if self.replied_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f'<Application {self.id} - {self.status}>'
