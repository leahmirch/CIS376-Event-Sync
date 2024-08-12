import unittest
from datetime import datetime
from flask import json
from backend.models import db, User, Event
from eventsync_app import app

class EventApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.create_test_user()
        self.create_test_event()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_test_user(self):
        test_user = User(username='testuser', email='testuser@example.com', password_hash='password')
        db.session.add(test_user)
        db.session.commit()
        self.user_id = test_user.id

    def create_test_event(self):
        test_event = Event(
            name='Test Event',
            description='This is a test event',
            start_datetime=datetime(2024, 1, 1, 9, 0),
            end_datetime=datetime(2024, 1, 1, 17, 0),
            location='Test Location',
            organizer_id=self.user_id
        )
        db.session.add(test_event)
        db.session.commit()
        self.event_id = test_event.id

    def test_get_events(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['_user_id'] = str(self.user_id)
            response = client.get('/api/events')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['name'], 'Test Event')

    def test_get_event(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['_user_id'] = str(self.user_id)
            response = client.get(f'/api/events/{self.event_id}')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['name'], 'Test Event')

    def test_delete_event(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['_user_id'] = str(self.user_id)
            response = client.delete(f'/api/events/{self.event_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Event deleted', json.loads(response.data)['success'])

if __name__ == '__main__':
    unittest.main()
