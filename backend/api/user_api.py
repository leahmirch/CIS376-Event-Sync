from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash
from backend.models import db, User

user_api = Blueprint('user_api', __name__)

@user_api.route('/api/users', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing data'}), 400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

@user_api.route('/register', methods=['GET', 'POST'])
def register_form():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('Please fill out all fields.')
            return redirect(url_for('user_api.register_form'))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists.')
            return redirect(url_for('user_api.register_form'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_api.register_success'))  # Redirect to the new success page

    return render_template('register.html')

@user_api.route('/register/success', methods=['GET'])
def register_success():
    return render_template('register_success.html')

def setup_user_api(app):
    app.register_blueprint(user_api)
