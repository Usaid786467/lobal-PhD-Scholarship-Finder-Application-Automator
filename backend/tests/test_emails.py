"""
Email Tests
Tests for email generation and batch management
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, University, Professor
from services.ai import GeminiService, EmailGenerator
from config import Config


@pytest.fixture
def app():
    """Create test app"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def auth_token(client):
    """Create authenticated user and return token"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User',
        'research_interests': ['Machine Learning', 'Deep Learning']
    })
    return response.get_json()['access_token']


@pytest.fixture
def test_professor(app):
    """Create test professor"""
    with app.app_context():
        uni = University(
            name='Test University',
            country='USA',
            website='https://test.edu'
        )
        db.session.add(uni)
        db.session.flush()

        prof = Professor(
            university_id=uni.id,
            name='Dr. Test Professor',
            email='professor@test.edu',
            department='Computer Science',
            research_interests='["Machine Learning", "AI"]'
        )
        db.session.add(prof)
        db.session.commit()

        return prof.id


def test_email_generator():
    """Test email generator"""
    gemini = GeminiService(Config.GEMINI_API_KEY)
    generator = EmailGenerator(gemini)

    email = generator.generate_email(
        professor_name='Dr. Smith',
        professor_research='Machine Learning, Deep Learning',
        university_name='MIT',
        user_name='John Doe',
        user_research='Deep Learning, AI'
    )

    assert 'subject' in email
    assert 'body' in email
    assert len(email['body']) > 50


def test_generate_emails_endpoint(client, auth_token, test_professor):
    """Test email generation endpoint"""
    response = client.post('/api/emails/generate',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'professor_ids': [test_professor]}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'batch_id' in data
    assert data['count'] == 1


def test_get_batches(client, auth_token):
    """Test getting email batches"""
    response = client.get('/api/emails/batches',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'batches' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
