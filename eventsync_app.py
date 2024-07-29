from flask import Flask
from config import Config

# Initialize the Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Sample route for the homepage
@app.route('/')
def home():
    return "Welcome to EventSync! The platform for efficient event management."

# Sample route for the dashboard (accessible after login)
@app.route('/dashboard')
def dashboard():
    return "This is your dashboard. All event management tools will be accessible here."

# Condition to run the application directly
if __name__ == '__main__':
    app.run(debug=True)
