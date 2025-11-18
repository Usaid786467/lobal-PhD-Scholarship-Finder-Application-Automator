"""
Professor Tests
Tests for professor routes and services
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, University, Professor


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
    """Create user and return auth token"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User',
        'research_interests': ['Machine Learning', 'Deep Learning']
    })
    return response.get_json()['access_token']


@pytest.fixture
def university(app):
    """Create test university"""
    with app.app_context():
        uni = University(
            name='Test University',
            country='US',
            website='https://test.edu',
            has_scholarship=True
        )
        db.session.add(uni)
        db.session.commit()
        return uni.id


def test_professor_search(client, auth_token, university):
    """Test professor search"""
    # Create a professor
    with client.application.app_context():
        prof = Professor(
            university_id=university,
            name='Dr. Test Professor',
            email='prof@test.edu',
            department='Engineering',
            research_interests='["Machine Learning", "Robotics"]'
        )
        db.session.add(prof)
        db.session.commit()

    response = client.get(
        f'/api/professors/search?university_id={university}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'professors' in data
    assert len(data['professors']) >= 1


def test_get_professor(client, auth_token, university):
    """Test getting individual professor"""
    # Create a professor
    with client.application.app_context():
        prof = Professor(
            university_id=university,
            name='Dr. Test Professor',
            email='prof@test.edu'
        )
        db.session.add(prof)
        db.session.commit()
        prof_id = prof.id

    response = client.get(
        f'/api/professors/{prof_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Dr. Test Professor'


def test_professor_stats(client, auth_token, university):
    """Test professor statistics"""
    # Create professors
    with client.application.app_context():
        for i in range(3):
            prof = Professor(
                university_id=university,
                name=f'Dr. Professor {i}',
                email=f'prof{i}@test.edu',
                accepting_students=(i % 2 == 0)
            )
            db.session.add(prof)
        db.session.commit()

    response = client.get(
        '/api/professors/stats',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] >= 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
