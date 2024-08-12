import pytest
import sys
import os
from werkzeug.security import generate_password_hash

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from eventsync_app import create_app, db
from backend.models import User, Event

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Set up initial database for the test."""
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='testuser@example.com', password_hash=generate_password_hash('testpassword'))
        db.session.add(user)
        db.session.commit()

        yield db

        db.drop_all()

def test_user_login(client, init_database):
    """Test that a user can log in."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200 or response.status_code == 302  # Check for success or redirect

def test_event_creation_without_login(client):
    """Test that event creation is forbidden without login."""
    response = client.post('/api/events', json=dict(
        name='Unauthorized Event',
        description='This event should not be created',
        date='2024-08-13 14:00',
        location='Unauthorized Location'
    ))
    assert response.status_code == 302  # Should redirect to login or show forbidden

def test_dashboard_access_without_login(client):
    """Test that the dashboard cannot be accessed without login."""
    response = client.get('/dashboard')
    assert response.status_code == 302  # Should redirect to login

def test_registration_page_access(client):
    """Test access to the registration page."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data  # Check if the page contains 'Register'
