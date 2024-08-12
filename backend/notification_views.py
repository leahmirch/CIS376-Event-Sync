from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from backend.models import db, Notification

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notification/read/<int:notification_id>', methods=['GET'])
@login_required
def read_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
    return redirect(url_for('main.dashboard'))
