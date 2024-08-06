from flask import Flask, Blueprint, request, redirect, render_template, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import db, User
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create a Blueprint for authentication
auth = Blueprint('auth', __name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Setup the login manager
def setup_login_manager(app):
    login_manager.init_app(app)

# Routes for authentication
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        logging.debug(f"Login attempt with username: {username}")  # Log username attempt

        user = User.query.filter_by(username=username).first()
        logging.debug(f"User found in DB: {user is not None}")  # Confirm user lookup
        if not user:
            flash('Username does not exist. Please register.', 'error')
            return render_template('login.html')

        if not check_password_hash(user.password_hash, password):
            logging.debug("Password hash check failed")  # Log failed password check
            flash('Password is incorrect. Please try again.', 'error')
            return render_template('login.html')

        login_user(user, remember=True)
        logging.debug("User logged in successfully")  # Confirm successful login
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists. Please login or use a different username/email.', 'error')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'info')
        return redirect(url_for('user_api.user_register_success'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('user_logout_success.html')

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key20'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventsync.db'  # Correct path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(auth)
    setup_login_manager(app)
    app.run(debug=True)


from flask import Flask
from backend.models import db
from backend.auth import setup_login_manager
from backend.views import setup_routes
from backend.vendor_views import setup_vendor_routes
from backend.payment_views import setup_payment_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key20'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventsync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
setup_login_manager(app)
setup_routes(app)
setup_vendor_routes(app)
setup_payment_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
