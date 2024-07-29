from flask import Blueprint, request, jsonify, abort
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

# Create a Blueprint for the user API
user_api = Blueprint('user_api', __name__)

@user_api.route('/api/users', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing data'}), 400

    # Check if the username or email already exists
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'user': {'username': new_user.username, 'email': new_user.email}}), 201

@user_api.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    if user_id != current_user.id:
        abort(403)  # Forbidden access if not the current user

    user = User.query.get_or_404(user_id)
    return jsonify({'username': user.username, 'email': user.email}), 200

@user_api.route('/api/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    if user_id != current_user.id:
        abort(403)  # Forbidden access if not the current user

    data = request.get_json()
    user = User.query.get_or_404(user_id)
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already in use'}), 409
        user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully', 'user': {'username': user.username, 'email': user.email}}), 200

def setup_user_api(app):
    app.register_blueprint(user_api)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    db.init_app(app)
    setup_user_api(app)
    app.run(debug=True)
