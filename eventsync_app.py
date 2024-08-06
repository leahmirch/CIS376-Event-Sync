from flask import Flask, render_template
from config.config import Config
from backend.models import db
from backend.auth import auth, setup_login_manager
from backend.views import main, setup_routes
from backend.api.event_api import setup_event_api
from backend.api.user_api import setup_user_api
from backend.vendor_views import setup_vendor_routes
from backend.payment_views import setup_payment_routes
from flask_migrate import Migrate

# Initialize the Flask application
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

# Load configuration from config.py
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Set up Flask-Migrate
migrate = Migrate(app, db)

# Set up login manager
setup_login_manager(app)

# Register blueprints
app.register_blueprint(auth)  # Register the auth blueprint
setup_routes(app)
setup_event_api(app)
setup_user_api(app)
setup_vendor_routes(app)  # Register vendor blueprint
setup_payment_routes(app)  # Register payment blueprint

# Sample route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create all tables based on models
        print("Initialized the database.")

# Condition to run the application directly
if __name__ == '__main__':
    app.run(debug=True)
