"""
Professor model for storing professor profile information
"""
from datetime import datetime
from models.database import db
import json


class Professor(db.Model):
    """Professor model for storing professor profiles"""

    __tablename__ = 'professors'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False, index=True)

    # Basic Information
    name = db.Column(db.String(150), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=True)  # e.g., Associate Professor, Full Professor
    email = db.Column(db.String(120), nullable=True, index=True)
    department = db.Column(db.String(150), nullable=True)

    # Research Information
    research_interests = db.Column(db.Text, nullable=True)  # JSON array
    publications = db.Column(db.Text, nullable=True)  # JSON array of publication objects

    # Academic Metrics
    h_index = db.Column(db.Integer, nullable=True)
    citations = db.Column(db.Integer, nullable=True)

    # Availability
    accepting_students = db.Column(db.Boolean, default=None, nullable=True)

    # URLs
    lab_website = db.Column(db.String(255), nullable=True)
    profile_url = db.Column(db.String(255), nullable=True)
    google_scholar_url = db.Column(db.String(255), nullable=True)
    researchgate_url = db.Column(db.String(255), nullable=True)

    # Additional Information
    photo_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_contacted = db.Column(db.DateTime, nullable=True)

    # Relationships
    applications = db.relationship('Application', backref='professor', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, name, university_id, **kwargs):
        """Initialize professor with required fields"""
        self.name = name
        self.university_id = university_id
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_research_interests(self, interests):
        """Set research interests from list"""
        if isinstance(interests, list):
            self.research_interests = json.dumps(interests)
        elif isinstance(interests, str):
            self.research_interests = interests

    def get_research_interests(self):
        """Get research interests as list"""
        if self.research_interests:
            try:
                return json.loads(self.research_interests)
            except:
                return []
        return []

    def set_publications(self, publications):
        """Set publications from list"""
        if isinstance(publications, list):
            self.publications = json.dumps(publications)
        elif isinstance(publications, str):
            self.publications = publications

    def get_publications(self):
        """Get publications as list"""
        if self.publications:
            try:
                return json.loads(self.publications)
            except:
                return []
        return []

    def add_publication(self, publication):
        """Add a single publication"""
        pubs = self.get_publications()
        pubs.append(publication)
        self.set_publications(pubs)

    def update_last_contacted(self):
        """Update last contacted timestamp"""
        self.last_contacted = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def calculate_match_score(self, user_interests):
        """
        Calculate match score with user research interests
        Returns score between 0-100
        """
        if not user_interests or not self.research_interests:
            return 0

        prof_interests = self.get_research_interests()
        if not prof_interests:
            return 0

        # Convert to lowercase for comparison
        user_interests_lower = [interest.lower() for interest in user_interests]
        prof_interests_lower = [interest.lower() for interest in prof_interests]

        # Calculate overlap
        matches = 0
        for user_interest in user_interests_lower:
            for prof_interest in prof_interests_lower:
                if user_interest in prof_interest or prof_interest in user_interest:
                    matches += 1
                    break

        # Calculate percentage
        score = (matches / len(user_interests)) * 100 if user_interests else 0
        return min(100, int(score))

    def to_dict(self, include_university=False, user_interests=None):
        """Convert professor to dictionary"""
        data = {
            'id': self.id,
            'university_id': self.university_id,
            'name': self.name,
            'title': self.title,
            'email': self.email,
            'department': self.department,
            'research_interests': self.get_research_interests(),
            'publications': self.get_publications(),
            'h_index': self.h_index,
            'citations': self.citations,
            'accepting_students': self.accepting_students,
            'lab_website': self.lab_website,
            'profile_url': self.profile_url,
            'google_scholar_url': self.google_scholar_url,
            'researchgate_url': self.researchgate_url,
            'photo_url': self.photo_url,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_contacted': self.last_contacted.isoformat() if self.last_contacted else None,
            'application_count': self.applications.count()
        }

        if include_university and self.university:
            data['university'] = self.university.to_dict()

        if user_interests:
            data['match_score'] = self.calculate_match_score(user_interests)

        return data

    def __repr__(self):
        """String representation"""
        return f'<Professor {self.name} at {self.university.name if self.university else "Unknown"}>'
