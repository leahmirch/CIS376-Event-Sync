from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from backend.models import db, User, Event, RSVP, Vendor, Payment, Feedback, Community, Notification
from datetime import datetime
from flask import abort
from backend.utils import create_notification
import csv
import json
import io

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    events = Event.query.filter_by(organizer_id=current_user.id).all()
    rsvps = RSVP.query.filter_by(user_id=current_user.id).all()
    user_communities = current_user.communities
    all_communities = Community.query.all()
    joinable_communities = [c for c in all_communities if c not in user_communities and c.creator_id != current_user.id]
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', events=events, rsvps=rsvps, user_communities=user_communities, joinable_communities=joinable_communities, notifications=notifications)

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
        vendor_ids = request.form.getlist('vendor_ids')
        payment_required = request.form.get('payment_required') == 'on'
        payment_amount = request.form['payment_amount'] if payment_required else 0

        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')
            
            new_event = Event(
                name=event_name,
                description=event_description,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                location=event_location,
                organizer_id=current_user.id,
                payment_required=payment_required,
                payment_amount=payment_amount
            )
            db.session.add(new_event)
            db.session.commit()
            
            for vendor_id in vendor_ids:
                vendor = Vendor.query.get(vendor_id)
                new_event.vendors.append(vendor)
            db.session.commit()
            
            create_notification(current_user.id, f"You have created a new event: {event_name}")

            flash('Event created successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'danger')

    vendors = Vendor.query.all()
    return render_template('create_event.html', vendors=vendors)

@main.route('/event/<int:event_id>')
@login_required
def event(event_id):
    event = Event.query.get_or_404(event_id)
    rsvps = RSVP.query.filter_by(event_id=event.id).all()
    total_collected = event.total_collected()
    feedbacks = Feedback.query.filter_by(event_id=event.id).all()
    invited_user_ids = [invitee.user_id for invitee in rsvps]
    users = User.query.filter(User.id.notin_(invited_user_ids)).all()
    return render_template('event.html', event=event, rsvps=rsvps, users=users, total_collected=total_collected, feedbacks=feedbacks)

@main.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        event.name = request.form['event_name']
        event.description = request.form['event_description']
        event.start_datetime = datetime.strptime(request.form['start_date'] + ' ' + request.form['start_time'], '%Y-%m-%d %H:%M')
        event.end_datetime = datetime.strptime(request.form['end_date'] + ' ' + request.form['end_time'], '%Y-%m-%d %H:%M')
        event.location = request.form['event_location']
        vendor_ids = request.form.getlist('vendor_ids')
        event.payment_required = request.form.get('payment_required') == 'on'
        event.payment_amount = request.form['payment_amount'] if event.payment_required else 0

        try:
            event.vendors = []
            for vendor_id in vendor_ids:
                vendor = Vendor.query.get(vendor_id)
                event.vendors.append(vendor)
            db.session.commit()

            create_notification(current_user.id, f"You have edited the event: {event.name}")

            flash('Event updated successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating event: {str(e)}', 'danger')

    vendors = Vendor.query.all()
    return render_template('edit_event.html', event=event, vendors=vendors)

@main.route('/event/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()

    create_notification(current_user.id, f"The event {event.name} has been deleted")

    flash('Event deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/event/<int:event_id>/invitees')
@login_required
def view_invitees(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    
    invitees = RSVP.query.filter_by(event_id=event.id).all()
    invited_user_ids = [invitee.user_id for invitee in invitees]
    users = User.query.filter(User.id.notin_(invited_user_ids)).all()
    
    return render_template('view_invitees.html', event=event, invitees=invitees, users=users)

@main.route('/event/<int:event_id>/invite', methods=['POST'])
@login_required
def invite_people(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        abort(403)
    
    selected_user_ids = request.form.getlist('invitees')
    
    for user_id in selected_user_ids:
        invite = RSVP(user_id=user_id, event_id=event_id, status='Pending')
        db.session.add(invite)
        create_notification(user_id, f"You have been invited to an event: {event.name}.")
    
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
    payment = Payment.query.filter_by(event_id=event_id, user_id=current_user.id).first()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'accept':
            if event.payment_required and (not payment or payment.status != 'Completed'):
                payment = Payment(
                    amount=event.payment_amount,
                    status='Pending',
                    user_id=current_user.id,
                    event_id=event_id
                )
                db.session.add(payment)
            rsvp.status = 'Accepted'
            db.session.commit()

            create_notification(event.organizer_id, f"{current_user.username} has accepted the invitation to the event: {event.name}")

            return redirect(url_for('user_api.accept_success', event_id=event.id))
        elif action == 'decline':
            rsvp.status = 'Declined'
            db.session.commit()

            create_notification(event.organizer_id, f"{current_user.username} has declined the invitation to the event: {event.name}")

            return redirect(url_for('user_api.decline_success', event_id=event.id))

    return render_template('view_event.html', event=event, rsvp=rsvp, payment=payment)

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/social/<int:event_id>')
@login_required
def social(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('social.html', event=event)

@main.route('/calendar/<int:event_id>')
@login_required
def calendar(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('calendar.html', event=event)

@main.route('/feedback/<int:event_id>', methods=['GET', 'POST'])
@login_required
def feedback(event_id):
    if request.method == 'POST':
        comment = request.form['comment']
        rating = request.form['rating']
        feedback = Feedback(user_id=current_user.id, event_id=event_id, comment=comment, rating=rating)
        db.session.add(feedback)
        db.session.commit()

        create_notification(event.organizer_id, f"New feedback for event: {event.name}")

        flash('Feedback submitted successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    event = Event.query.get_or_404(event_id)
    return render_template('feedback.html', event=event)

@main.route('/event/<int:event_id>/view_feedbacks')
@login_required
def view_feedbacks(event_id):
    event = Event.query.get_or_404(event_id)
    feedbacks = Feedback.query.filter_by(event_id=event.id).all()
    return render_template('view_feedbacks.html', event=event, feedbacks=feedbacks)

@main.route('/clear_notifications', methods=['POST'])
@login_required
def clear_notifications():
    Notification.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('All notifications cleared.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/event/<int:event_id>/export')
@login_required
def export_page(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('export.html', event=event)

@main.route('/event/<int:event_id>/export/csv')
@login_required
def export_event_csv(event_id):
    event = Event.query.get_or_404(event_id)
    output = io.StringIO()
    writer = csv.writer(output)

    # Writing the event details
    writer.writerow(['Event Name', 'Description', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Location', 'Total Collected'])
    writer.writerow([event.name, event.description, event.start_datetime.strftime('%Y-%m-%d'), event.start_datetime.strftime('%I:%M %p'), event.end_datetime.strftime('%Y-%m-%d'), event.end_datetime.strftime('%I:%M %p'), event.location, event.total_collected()])

    # Writing the RSVPs
    writer.writerow([])
    writer.writerow(['RSVPs'])
    writer.writerow(['User', 'Status'])
    for rsvp in event.rsvps:
        writer.writerow([rsvp.user.username, rsvp.status])

    # Writing the Vendors
    writer.writerow([])
    writer.writerow(['Vendors'])
    writer.writerow(['Name', 'Contact Info', 'Contract Details'])
    for vendor in event.vendors:
        writer.writerow([vendor.name, vendor.contact_info, vendor.contract_details])

    # Writing the Feedback
    writer.writerow([])
    writer.writerow(['Feedback'])
    writer.writerow(['User', 'Comment', 'Rating'])
    for feedback in event.feedbacks:
        writer.writerow([feedback.user.username, feedback.comment, feedback.rating])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name=f'{event.name}_event_data.csv')

@main.route('/event/<int:event_id>/export/json')
@login_required
def export_event_json(event_id):
    event = Event.query.get_or_404(event_id)
    event_data = {
        'name': event.name,
        'description': event.description,
        'start_date': event.start_datetime.strftime('%Y-%m-%d'),
        'start_time': event.start_datetime.strftime('%I:%M %p'),
        'end_date': event.end_datetime.strftime('%Y-%m-%d'),
        'end_time': event.end_datetime.strftime('%I:%M %p'),
        'location': event.location,
        'total_collected': event.total_collected(),
        'rsvps': [{'user': rsvp.user.username, 'status': rsvp.status} for rsvp in event.rsvps],
        'vendors': [{'name': vendor.name, 'contact_info': vendor.contact_info, 'contract_details': vendor.contract_details} for vendor in event.vendors],
        'feedback': [{'user': feedback.user.username, 'comment': feedback.comment, 'rating': feedback.rating} for feedback in event.feedbacks]
    }

    response = jsonify(event_data)
    response.headers.add('Content-Disposition', 'attachment; filename=' + f'{event.name}_event_data.json')
    return response

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