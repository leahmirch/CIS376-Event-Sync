from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from models import db, Event
from datetime import datetime

# Create a Blueprint for the event API
event_api = Blueprint('event_api', __name__)

@event_api.route('/api/events', methods=['GET'])
@login_required
def get_events():
    events = Event.query.filter_by(organizer_id=current_user.id).all()
    return jsonify([event.to_dict() for event in events]), 200

@event_api.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        new_event = Event(
            name=data['name'],
            description=data.get('description', ''),
            date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M'),
            location=data['location'],
            organizer_id=current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201

    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid data', 'message': str(e)}), 400

@event_api.route('/api/events/<int:event_id>', methods=['GET'])
@login_required
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    return jsonify(event.to_dict()), 200

@event_api.route('/api/events/<int:event_id>', methods=['PUT'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    
    data = request.get_json()
    try:
        event.name = data['name']
        event.description = data.get('description', event.description)
        event.date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M')
        event.location = data['location']
        db.session.commit()
        return jsonify(event.to_dict()), 200
    except KeyError as e:
        return jsonify({'error': 'Invalid data', 'message': str(e)}), 400

@event_api.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    
    db.session.delete(event)
    db.session.commit()
    return jsonify({'success': 'Event deleted'}), 200

def setup_event_api(app):
    app.register_blueprint(event_api)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    db.init_app(app)
    setup_event_api(app)
    app.run(debug=True)
