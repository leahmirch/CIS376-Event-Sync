from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

# Create a Blueprint for authentication
auth = Blueprint('auth', __name__)

# Initialize Flask-Login
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Setup the login manager
login_manager.login_view = 'auth.login'

# Routes for authentication
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

def setup_login_manager(app):
    login_manager.init_app(app)

# Additional authentication helper functions can be added here

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    db.init_app(app)
    app.register_blueprint(auth)
    setup_login_manager(app)
    app.run(debug=True)
