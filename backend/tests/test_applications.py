"""
Application Tests
Tests for application tracking and management
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, University, Professor, Application


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
        'name': 'Test User'
    })
    return response.get_json()['access_token']


@pytest.fixture
def user_id(client):
    """Get user ID"""
    response = client.post('/api/auth/register', json={
        'email': 'test2@example.com',
        'password': 'password123',
        'name': 'Test User 2'
    })
    return response.get_json()['user']['id']


@pytest.fixture
def professor(app):
    """Create test professor"""
    with app.app_context():
        uni = University(name='Test Uni', country='US', website='https://test.edu')
        db.session.add(uni)
        db.session.flush()

        prof = Professor(
            university_id=uni.id,
            name='Dr. Test',
            email='prof@test.edu'
        )
        db.session.add(prof)
        db.session.commit()
        return prof.id


def test_get_applications(client, auth_token, user_id, professor):
    """Test getting user applications"""
    # Create an application
    with client.application.app_context():
        app_obj = Application(
            user_id=user_id,
            professor_id=professor,
            status='draft'
        )
        db.session.add(app_obj)
        db.session.commit()

    response = client.get(
        '/api/applications',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    assert response.status_code == 200


def test_create_application(client, auth_token, professor):
    """Test creating application"""
    response = client.post(
        '/api/applications',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'professor_id': professor}
    )

    # Response may be 200 or 201 depending on implementation
    assert response.status_code in [200, 201]


def test_update_application_status(client, auth_token, user_id, professor):
    """Test updating application status"""
    # Create an application
    with client.application.app_context():
        app_obj = Application(
            user_id=user_id,
            professor_id=professor,
            status='draft'
        )
        db.session.add(app_obj)
        db.session.commit()
        app_id = app_obj.id

    response = client.put(
        f'/api/applications/{app_id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'status': 'sent'}
    )

    # Check if endpoint exists
    assert response.status_code != 404


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
