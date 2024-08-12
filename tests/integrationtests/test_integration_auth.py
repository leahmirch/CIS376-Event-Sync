import unittest
from flask import url_for
from eventsync_app import app, db
from backend.models import User
from werkzeug.security import generate_password_hash

class AuthIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'localhost.localdomain'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()

            # Create a test user with a hashed password
            hashed_password = generate_password_hash("testpassword")
            test_user = User(username="testuser", email="testuser@example.com", password_hash=hashed_password)
            db.session.add(test_user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        """Push an application context before each test."""
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Pop the application context after each test."""
        self.app_context.pop()

    def test_registration_page_loads(self):
        """Test that the registration page loads correctly."""
        response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page_loads(self):
        """Test that the login page loads correctly."""
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_successful_login(self):
        """Test that a user can log in with correct credentials."""
        response = self.client.post(url_for('auth.login'), data=dict(
            username="testuser",
            password="testpassword"
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_successful_logout(self):
        """Test that a logged-in user can log out successfully."""
        self.client.post(url_for('auth.login'), data=dict(
            username="testuser",
            password="testpassword"
        ), follow_redirects=True)

        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been successfully logged out', response.data)

if __name__ == '__main__':
    unittest.main()
