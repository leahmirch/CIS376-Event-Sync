import unittest
from flask import Flask
from backend.models import db, Notification, User
from backend.utils import create_notification

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up a temporary SQLite database and Flask app for testing."""
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = 'test_secret'
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()
            # Create a test user and add it to the session
            self.user = User(username="testuser", email="test@example.com", password_hash="hashed")
            db.session.add(self.user)
            db.session.commit()
            db.session.refresh(self.user)  # Ensure the user is attached to the session

    def tearDown(self):
        """Clean up the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_notification(self):
        """Test that create_notification correctly creates a new notification."""
        with self.app.app_context():
            create_notification(user_id=self.user.id, message="Test notification")
            notification = Notification.query.filter_by(user_id=self.user.id).first()
            self.assertIsNotNone(notification)
            self.assertEqual(notification.message, "Test notification")

if __name__ == '__main__':
    unittest.main()
