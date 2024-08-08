# payment_views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from backend.models import db, Payment, Event, RSVP
from backend.utils import create_notification

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/pay/<int:event_id>', methods=['GET', 'POST'])
@login_required
def pay(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        return jsonify({'redirect': 'https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=mirchleah20@yahoo.com&amount={}&currency_code=USD'.format(event.payment_amount)})

@payment_bp.route('/execute/<int:event_id>', methods=['GET'])
@login_required
def execute_payment(event_id):
    payment = Payment.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if payment:
        payment.status = 'Completed'
        db.session.commit()

        # Notify event organizer
        create_notification(event.organizer_id, f"Payment received for event: {event.name}")

        flash('Payment successful!', 'success')
    else:
        flash('Payment not found.', 'danger')
    return redirect(url_for('main.dashboard'))

@payment_bp.route('/pay_and_accept/<int:event_id>', methods=['POST'])
@login_required
def pay_and_accept(event_id):
    event = Event.query.get_or_404(event_id)
    rsvp = RSVP.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    
    payment = Payment(
        amount=event.payment_amount,
        status='Pending',
        user_id=current_user.id,
        event_id=event_id
    )
    db.session.add(payment)
    db.session.commit()
    
    return jsonify({'redirect': 'https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=mirchleah20@yahoo.com&amount={}&currency_code=USD'.format(event.payment_amount)})

def setup_payment_routes(app):
    app.register_blueprint(payment_bp)
