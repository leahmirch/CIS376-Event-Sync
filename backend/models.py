from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='organizer', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(140))
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rsvps = db.relationship('RSVP', backref='event', lazy='dynamic')

    def __repr__(self):
        return '<Event {}>'.format(self.name)

class RSVP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    status = db.Column(db.String(64))

    def __repr__(self):
        return '<RSVP for Event {} by User {}>'.format(self.event_id, self.user_id)

# Additional models like Vendor or Feedback can be added following similar patterns.
