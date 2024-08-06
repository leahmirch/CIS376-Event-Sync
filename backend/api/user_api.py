from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash
from backend.models import db, User, Event  # Import the Event model

user_api = Blueprint('user_api', __name__)

@user_api.route('/user_register_success', methods=['GET'])
def user_register_success():
    return render_template('user_register_success.html')

@user_api.route('/accept_success/<int:event_id>', methods=['GET'])
def accept_success(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('accept_success.html', event=event)

@user_api.route('/decline_success/<int:event_id>', methods=['GET'])
def decline_success(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('decline_success.html', event=event)

def setup_user_api(app):
    app.register_blueprint(user_api)
