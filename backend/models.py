from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='organizer', lazy='dynamic')
    rsvps = db.relationship('RSVP', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.Text)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    location = db.Column(db.String(140))
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rsvps = db.relationship('RSVP', backref='event', lazy='dynamic')

    def __repr__(self):
        return '<Event {}>'.format(self.name)

class RSVP(db.Model):
    __tablename__ = 'rsvps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    status = db.Column(db.String(64))

    def __repr__(self):
        return '<RSVP for Event {} by User {}>'.format(self.event_id, self.user_id)
