import unittest
from flask import Flask 
from datetime import datetime
from backend.models import db, User, Event, Payment

class TestModels(unittest.TestCase):
    def setUp(self):
        """Set up a temporary SQLite database for testing."""
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        """Test that a User can be created and is_active returns True."""
        with self.app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed")
            db.session.add(user)
            db.session.commit()

            # Check that the user was added and is active
            self.assertTrue(user.is_active())
            self.assertEqual(User.query.count(), 1)

    def test_event_total_collected(self):
        """Test that total_collected correctly sums up completed payments."""
        with self.app.app_context():
            event = Event(name="Test Event", description="Description", start_datetime=datetime.utcnow(), end_datetime=datetime.utcnow(), location="Location", organizer_id=1)
            db.session.add(event)
            db.session.commit()

            payment1 = Payment(amount=50.0, status='Completed', user_id=1, event_id=event.id)
            payment2 = Payment(amount=75.0, status='Completed', user_id=2, event_id=event.id)
            payment3 = Payment(amount=25.0, status='Pending', user_id=3, event_id=event.id)
            db.session.add_all([payment1, payment2, payment3])
            db.session.commit()

            self.assertEqual(event.total_collected(), 125.0)

if __name__ == '__main__':
    unittest.main()
