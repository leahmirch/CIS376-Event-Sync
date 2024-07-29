import unittest
from flask import Flask, session
from models import db, User, Event
from auth import setup_login_manager
from views import setup_routes
from event_api import setup_event_api
from user_api import setup_user_api

class EventSyncTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and initialize the database with test data."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = 'testkey'

        # Initialize components
        db.init_app(self.app)
        setup_login_manager(self.app)
        setup_routes(self.app)
        setup_event_api(self.app)
        setup_user_api(self.app)

        # Create test client
        self.client = self.app.test_client()

        # Create tables and add sample data
        with self.app.app_context():
            db.create_all()
            self.create_sample_data()

    def tearDown(self):
        """Cleanup after tests."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_sample_data(self):
        """Create sample data for testing."""
        user1 = User(username='testuser1', email='test1@example.com', password_hash='hashedpassword1')
        user2 = User(username='testuser2', email='test2@example.com', password_hash='hashedpassword2')
        event1 = Event(name='Test Event 1', description='A test event', date='2021-09-01 12:00', location='Test Location', organizer=user1)
        db.session.add_all([user1, user2, event1])
        db.session.commit()

    def test_home_page(self):
        """Test that the home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to EventSync!', response.data.decode())

    def test_dashboard_access(self):
        """Test that the dashboard page requires user login."""
        response = self.client.get('/dashboard')
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue('Login' in response.data.decode())

    def test_event_creation(self):
        """Test creating an event via form submission."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Simulate login
            response = client.post('/event/new', data=dict(
                name='New Event',
                description='Description for new event',
                date='2021-10-01 12:00',
                location='New Location'
            ), follow_redirects=True)
            self.assertIn('Event created successfully!', response.data.decode())

    # Additional tests for login, registration, event updates, and deletions can be added here

if __name__ == '__main__':
    unittest.main()
