"""
University Model
Stores university information from scraping
"""
from datetime import datetime
from models import db


class University(db.Model):
    """University model for storing scraped university data"""

    __tablename__ = 'universities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    country = db.Column(db.String(100), nullable=False, index=True)
    website = db.Column(db.String(500))
    has_scholarship = db.Column(db.Boolean, default=False)
    scholarship_info = db.Column(db.Text)  # JSON string of scholarship details
    deadline = db.Column(db.Date)
    research_areas = db.Column(db.Text)  # JSON string of research areas
    contact_info = db.Column(db.Text)  # JSON string of contact details
    ranking = db.Column(db.Integer)
    location = db.Column(db.String(255))

    # Scraping metadata
    last_scraped = db.Column(db.DateTime, default=datetime.utcnow)
    scrape_status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    professors = db.relationship('Professor', backref='university', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self) -> dict:
        """Convert university to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'website': self.website,
            'has_scholarship': self.has_scholarship,
            'scholarship_info': self.scholarship_info,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'research_areas': self.research_areas,
            'contact_info': self.contact_info,
            'ranking': self.ranking,
            'location': self.location,
            'professor_count': self.professors.count(),
            'last_scraped': self.last_scraped.isoformat() if self.last_scraped else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f'<University {self.name} ({self.country})>'
