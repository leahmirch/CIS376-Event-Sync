import unittest
from flask import Flask
from backend.forms import FeedbackForm

class TestFeedbackForm(unittest.TestCase):
    def setUp(self):
        """Set up a Flask app context for testing."""
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'key20'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        """Tear down the Flask app context."""
        self.ctx.pop()

    def test_feedback_form_valid_data(self):
        """Test FeedbackForm with valid data."""
        form_data = {
            'content': 'This is feedback content.',
            'rating': 4
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
