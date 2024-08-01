from werkzeug.security import generate_password_hash
from backend.models import db, User
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventsync.db'  # Correct path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def add_user_to_db(username, email, plain_password):
    hashed_password = generate_password_hash(plain_password)
    user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

with app.app_context():
    db.drop_all()  # Drop all tables to avoid duplicates
    db.create_all()  # Recreate all tables
    add_user_to_db('admin', 'admin@example.com', 'password')
    add_user_to_db('organizer', 'organizer@example.com', 'password')
    print("Users added to the database.")
