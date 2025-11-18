"""
Pytest configuration and shared fixtures
"""
import pytest
import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture
def app():
    """Create application instance for testing"""
    # TODO: Implement after creating Flask app
    pass


@pytest.fixture
def client(app):
    """Create test client"""
    # TODO: Implement after creating Flask app
    pass


@pytest.fixture
def db():
    """Create database for testing"""
    # TODO: Implement after setting up database
    pass


@pytest.fixture
def session(db):
    """Create database session for testing"""
    # TODO: Implement after setting up database
    pass


@pytest.fixture
def user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "Test123!@#",
        "name": "Test User",
        "research_interests": ["Deep Learning", "Manufacturing", "Aerospace"]
    }


@pytest.fixture
def university_data():
    """Sample university data for testing"""
    return {
        "name": "Massachusetts Institute of Technology",
        "country": "USA",
        "city": "Cambridge",
        "website": "https://mit.edu",
        "has_scholarship": True,
        "scholarship_details": "Full funding available"
    }


@pytest.fixture
def professor_data():
    """Sample professor data for testing"""
    return {
        "name": "Dr. John Smith",
        "email": "jsmith@university.edu",
        "department": "Mechanical Engineering",
        "research_interests": ["Deep Learning", "Manufacturing Optimization"],
        "accepting_students": True
    }


@pytest.fixture
def email_data():
    """Sample email data for testing"""
    return {
        "subject": "PhD Opportunity - Research Interest",
        "body": "Dear Professor...",
        "status": "draft"
    }


# Test database configuration
TEST_DATABASE_URL = "sqlite:///:memory:"

# Test API configuration
TEST_API_BASE_URL = "http://localhost:5000/api"

# Mock Gemini API key for testing
TEST_GEMINI_API_KEY = "test_api_key_for_testing"
