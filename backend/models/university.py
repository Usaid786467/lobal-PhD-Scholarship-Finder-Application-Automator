"""
University Model for PhD Application Automator
Stores information about universities and programs
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class University(Base):
    """University model for storing institution information"""

    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True)

    # Basic Information
    name = Column(String(500), nullable=False, index=True)
    country = Column(String(100), nullable=False, index=True)
    city = Column(String(255))
    state_province = Column(String(255))
    website = Column(String(500))
    domain = Column(String(255))  # e.g., mit.edu, tsinghua.edu.cn

    # Rankings (nullable as not all universities are ranked)
    qs_ranking = Column(Integer)
    times_ranking = Column(Integer)
    arwu_ranking = Column(Integer)

    # Department Information
    department_name = Column(String(500))  # e.g., "Department of Mechanical Engineering"
    department_url = Column(String(500))
    school_name = Column(String(500))  # e.g., "School of Engineering"

    # Research Information
    research_areas = Column(JSON, default=list)  # List of research areas
    research_labs = Column(JSON, default=list)  # List of research labs/groups

    # Funding & Scholarship
    has_scholarship = Column(Boolean, default=False, index=True)
    scholarship_details = Column(Text)  # Detailed scholarship information
    scholarship_amount = Column(String(255))  # e.g., "$30,000/year"
    scholarship_url = Column(String(500))
    funding_types = Column(JSON, default=list)  # ["Fellowship", "RA", "TA", etc.]

    # Application Information
    application_deadline = Column(Date, index=True)
    application_url = Column(String(500))
    application_requirements = Column(JSON, default=list)
    accepts_international = Column(Boolean, default=True)
    english_requirement = Column(String(255))  # e.g., "TOEFL 90+ or IELTS 7.0+"

    # Contact Information
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    contact_address = Column(Text)
    admissions_office_email = Column(String(255))

    # Additional Info
    program_duration = Column(String(100))  # e.g., "4-6 years"
    degree_offered = Column(String(255))  # e.g., "PhD in Mechanical Engineering"
    language_of_instruction = Column(String(100), default="English")

    # Media
    logo_url = Column(String(500))
    image_url = Column(String(500))

    # Scraping Metadata
    last_scraped = Column(DateTime)
    scraping_status = Column(String(50))  # 'pending', 'completed', 'failed'
    scraping_errors = Column(Text)
    source_url = Column(String(500))  # URL where info was scraped from

    # Statistics
    professor_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)

    # Match Score (calculated for each user)
    match_score = Column(Float)  # 0-100 percentage

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Manually verified data

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Notes
    notes = Column(Text)  # Internal notes

    def to_dict(self, include_details=True):
        """Convert university to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'website': self.website,
            'domain': self.domain,
            'qs_ranking': self.qs_ranking,
            'has_scholarship': self.has_scholarship,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'match_score': self.match_score,
            'logo_url': self.logo_url,
            'professor_count': self.professor_count,
            'application_count': self.application_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_details:
            data.update({
                'state_province': self.state_province,
                'times_ranking': self.times_ranking,
                'arwu_ranking': self.arwu_ranking,
                'department_name': self.department_name,
                'department_url': self.department_url,
                'school_name': self.school_name,
                'research_areas': self.research_areas or [],
                'research_labs': self.research_labs or [],
                'scholarship_details': self.scholarship_details,
                'scholarship_amount': self.scholarship_amount,
                'scholarship_url': self.scholarship_url,
                'funding_types': self.funding_types or [],
                'application_url': self.application_url,
                'application_requirements': self.application_requirements or [],
                'accepts_international': self.accepts_international,
                'english_requirement': self.english_requirement,
                'contact_email': self.contact_email,
                'contact_phone': self.contact_phone,
                'admissions_office_email': self.admissions_office_email,
                'program_duration': self.program_duration,
                'degree_offered': self.degree_offered,
                'language_of_instruction': self.language_of_instruction,
                'image_url': self.image_url,
                'last_scraped': self.last_scraped.isoformat() if self.last_scraped else None,
                'notes': self.notes,
            })

        return data

    def calculate_match_score(self, user_interests, target_countries):
        """Calculate match score based on user preferences"""
        score = 0.0

        # Country match (30 points)
        if self.country in target_countries:
            score += 30

        # Scholarship availability (25 points)
        if self.has_scholarship:
            score += 25

        # Research area match (30 points)
        if self.research_areas and user_interests:
            # Count matching research areas
            user_areas_lower = [area.lower().strip() for area in user_interests]
            uni_areas_lower = [area.lower().strip() for area in self.research_areas]

            matches = sum(1 for area in user_areas_lower if any(ua in uni_area for ua in [area] for uni_area in uni_areas_lower))
            if matches > 0:
                score += min(matches * 10, 30)  # Max 30 points

        # Has professors (10 points)
        if self.professor_count > 0:
            score += 10

        # English instruction (5 points)
        if self.language_of_instruction and 'english' in self.language_of_instruction.lower():
            score += 5

        self.match_score = min(score, 100)  # Cap at 100
        return self.match_score

    def __repr__(self):
        return f'<University {self.name}, {self.country}>'
