"""
Authentication Tests
Tests for user registration, login, and profile management
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User


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


def test_register(client):
    """Test user registration"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User',
        'research_interests': ['Machine Learning', 'Deep Learning']
    })

    assert response.status_code == 201
    data = response.get_json()
    assert 'access_token' in data
    assert data['user']['email'] == 'test@example.com'


def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    # Register first user
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })

    # Try to register with same email
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password456',
        'name': 'Another User'
    })

    assert response.status_code == 400


def test_login(client):
    """Test user login"""
    # Register user
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })

    # Login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401


def test_get_profile(client):
    """Test getting user profile"""
    # Register and login
    reg_response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })

    token = reg_response.get_json()['access_token']

    # Get profile
    response = client.get('/api/auth/profile', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == 'test@example.com'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
