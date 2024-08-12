import unittest
from datetime import datetime
from werkzeug.security import generate_password_hash
from backend.models import db, User, Event
from eventsync_app import app

class UserApiTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        # Set up the application context and create tables
        with self.app.app_context():
            db.create_all()

            # Create a test user and event
            self.user = User(username='testuser', email='testuser@example.com', password_hash=generate_password_hash('password'))
            db.session.add(self.user)
            db.session.commit()

            self.event = Event(
                name='Test Event',
                description='This is a test event',
                start_datetime=datetime(2024, 1, 1, 9, 0),
                end_datetime=datetime(2024, 1, 1, 17, 0),
                location='Test Location',
                organizer_id=self.user.id
            )
            db.session.add(self.event)
            db.session.commit()

    def tearDown(self):
        # Clean up the database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_register_success(self):
        # Test the user registration success page
        response = self.client.get('/user_register_success')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration Successful', response.data)

    def test_accept_success(self):
        # Reattach event to session
        with self.app.app_context():
            event = db.session.merge(self.event)  # Reattach the event to the session
            response = self.client.get(f'/accept_success/{event.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invitation Accepted', response.data)  # Check for part of the message

    def test_decline_success(self):
        # Reattach event to session
        with self.app.app_context():
            event = db.session.merge(self.event)  # Reattach the event to the session
            response = self.client.get(f'/decline_success/{event.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invitation Declined', response.data)  # Check for part of the message

if __name__ == '__main__':
    unittest.main()
