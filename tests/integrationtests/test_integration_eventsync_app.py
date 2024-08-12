import unittest
from flask import url_for
from eventsync_app import app, db

class EventSyncAppIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'localhost.localdomain'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_home_page_loads(self):
        with app.app_context():
            response = self.client.get(url_for('home'))
            self.assertEqual(response.status_code, 200)

    def test_auth_blueprint_registration(self):
        with app.app_context():
            response = self.client.get(url_for('auth.login'))
            self.assertEqual(response.status_code, 200)

    def test_event_api_setup(self):
        with app.app_context():
            # Assuming event_api.get_events might redirect if no events are present
            response = self.client.get(url_for('event_api.get_events'))
            self.assertIn(response.status_code, [200, 302])

    def test_community_routes_setup(self):
        with app.app_context():
            response = self.client.get(url_for('community.index'))
            self.assertIn(response.status_code, [200, 302])

    def test_notification_blueprint_setup(self):
        with app.app_context():
            response = self.client.get(url_for('notification.read_notification', notification_id=1))
            self.assertIn(response.status_code, [200, 302])

if __name__ == '__main__':
    unittest.main()
