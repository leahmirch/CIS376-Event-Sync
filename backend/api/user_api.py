from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash
from backend.models import db, User

user_api = Blueprint('user_api', __name__)

@user_api.route('/user_register_success', methods=['GET'])
def user_register_success():
    return render_template('user_register_success.html')

def setup_user_api(app):
    app.register_blueprint(user_api)
