from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Association table for many-to-many relationship between events and vendors
event_vendor = db.Table('event_vendor',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('vendor_id', db.Integer, db.ForeignKey('vendors.id'), primary_key=True)
)

# Association table for many-to-many relationship between users and communities
user_community = db.Table('user_community',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('community_id', db.Integer, db.ForeignKey('communities.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    events = db.relationship('Event', backref='organizer', lazy=True)
    rsvps = db.relationship('RSVP', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    created_communities = db.relationship('Community', backref='creator', lazy=True)
    communities = db.relationship('Community', secondary=user_community, backref=db.backref('members', lazy='dynamic'))

    def is_active(self):
        return True

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(140), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vendors = db.relationship('Vendor', secondary=event_vendor, backref=db.backref('events', lazy='dynamic'))
    rsvps = db.relationship('RSVP', backref='event', lazy=True)
    payments = db.relationship('Payment', backref='event', lazy=True)
    feedbacks = db.relationship('Feedback', backref='event', lazy=True)
    payment_required = db.Column(db.Boolean, default=False)
    payment_amount = db.Column(db.Float, nullable=True)

    def total_collected(self):
        collected = sum(payment.amount for payment in self.payments if payment.status == 'Completed')
        return float(collected)

class RSVP(db.Model):
    __tablename__ = 'rsvps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    status = db.Column(db.String(64))

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    contact_info = db.Column(db.String(200), nullable=False)
    contract_details = db.Column(db.Text, nullable=False)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(64), nullable=False, default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Community(db.Model):
    __tablename__ = 'communities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    messages = db.relationship('CommunityMessage', backref='community', lazy=True, cascade="all, delete-orphan")

class CommunityMessage(db.Model):
    __tablename__ = 'community_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='community_messages')
