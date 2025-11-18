"""
Professor Model
Stores professor profiles and research information
"""
from datetime import datetime
from models import db


class Professor(db.Model):
    """Professor model for storing faculty information"""

    __tablename__ = 'professors'

    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(120), index=True)
    department = db.Column(db.String(255))
    research_interests = db.Column(db.Text)  # JSON string of research interests
    publications = db.Column(db.Text)  # JSON string of recent publications
    h_index = db.Column(db.Integer)
    accepting_students = db.Column(db.Boolean, default=True)
    profile_url = db.Column(db.String(500))
    google_scholar_url = db.Column(db.String(500))

    # Scraping metadata
    last_scraped = db.Column(db.DateTime, default=datetime.utcnow)
    scrape_status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='professor', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_match_score: bool = False) -> dict:
        """Convert professor to dictionary"""
        data = {
            'id': self.id,
            'university_id': self.university_id,
            'university_name': self.university.name if self.university else None,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'research_interests': self.research_interests,
            'publications': self.publications,
            'h_index': self.h_index,
            'accepting_students': self.accepting_students,
            'profile_url': self.profile_url,
            'google_scholar_url': self.google_scholar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        return data

    def __repr__(self) -> str:
        return f'<Professor {self.name}>'
