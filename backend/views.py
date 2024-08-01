from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.models import db, User, Event, RSVP
from datetime import datetime

# Create a Blueprint for the main part of the application
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Get all events organized by the current user
    events = Event.query.filter_by(organizer_id=current_user.id).all()
    return render_template('dashboard.html', events=events)

@main.route('/event/new', methods=['GET', 'POST'])
@login_required
def new_event():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d %H:%M')
        location = request.form['location']
        
        new_event = Event(name=name, description=description, date=date, location=location, organizer_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('new_event.html')

@main.route('/event/<int:event_id>')
@login_required
def event(event_id):
    event = Event.query.get_or_404(event_id)
    rsvps = RSVP.query.filter_by(event_id=event.id).all()
    return render_template('event.html', event=event, rsvps=rsvps)

@main.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.name = request.form['name']
        event.description = request.form['description']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d %H:%M')
        event.location = request.form['location']
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_event.html', event=event)

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/about')
def about():
    return render_template('about.html')
def setup_routes(app):
    app.register_blueprint(main)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key20'
    db.init_app(app)
    setup_routes(app)
    app.run(debug=True)
