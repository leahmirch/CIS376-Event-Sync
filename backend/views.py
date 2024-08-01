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
    events = Event.query.filter_by(organizer_id=current_user.id).all()
    rsvps = RSVP.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', events=events, rsvps=rsvps)

@main.route('/event/new', methods=['GET', 'POST'])
@login_required
def new_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_description = request.form['event_description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        event_location = request.form['event_location']

        try:
            new_event = Event(
                name=event_name,
                description=event_description,
                start_datetime=datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %I:%M %p'),
                end_datetime=datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %I:%M %p'),
                location=event_location,
                organizer_id=current_user.id
            )
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            flash(f'Error creating event: {str(e)}', 'danger')

    return render_template('create_event.html')

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
        event.start_datetime = datetime.strptime(request.form['start_date'] + ' ' + request.form['start_time'], '%Y-%m-%d %I:%M %p')
        event.end_datetime = datetime.strptime(request.form['end_date'] + ' ' + request.form['end_time'], '%Y-%m-%d %I:%M %p')
        event.location = request.form['location']
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_event.html', event=event)

@main.route('/event/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!')
    return redirect(url_for('main.dashboard'))

@main.route('/event/<int:event_id>/invitees')
@login_required
def view_invitees(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    
    # Fetch current invitees
    invitees = RSVP.query.filter_by(event_id=event.id).all()
    
    # Fetch all users excluding current invitees
    invited_user_ids = [invitee.user_id for invitee in invitees]
    users = User.query.filter(User.id.notin_(invited_user_ids)).all()
    
    return render_template('view_invitees.html', event=event, invitees=invitees, users=users)

@main.route('/event/<int:event_id>/invite', methods=['POST'])
@login_required
def invite_people(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    
    # Get selected users from the form
    selected_user_ids = request.form.getlist('invitees')
    
    for user_id in selected_user_ids:
        invite = RSVP(user_id=user_id, event_id=event_id, status='Pending')
        db.session.add(invite)
    
    db.session.commit()
    invited_users = User.query.filter(User.id.in_(selected_user_ids)).all()
    invited_usernames = [user.username for user in invited_users]
    flash(f'Invitations sent to: {", ".join(invited_usernames)}.', 'success')
    return redirect(url_for('main.view_invitees', event_id=event_id))

@main.route('/view_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    rsvp = RSVP.query.filter_by(event_id=event_id, user_id=current_user.id).first()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'accept':
            rsvp.status = 'Accepted'
            db.session.commit()
            return render_template('accept_success.html', event=event)
        elif action == 'decline':
            rsvp.status = 'Declined'
            db.session.commit()
            return render_template('decline_success.html', event=event)

    return render_template('view_event.html', event=event, rsvp=rsvp)

@main.route('/event/<int:event_id>/accept', methods=['POST'])
@login_required
def accept_invitation(event_id):
    rsvp = RSVP.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if rsvp:
        rsvp.status = 'Accepted'
        db.session.commit()
        flash('You have successfully accepted the invitation.', 'success')
    else:
        flash('Invitation not found.', 'error')
    return redirect(url_for('main.dashboard'))

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/about')
def about():
    return render_template('about.html')

def setup_routes(app):
    app.register_blueprint(main)

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key20'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventsync.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(main)
    setup_login_manager(app)
    app.run(debug=True)