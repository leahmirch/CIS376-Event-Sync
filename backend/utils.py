# backend/utils.py
from backend.models import db, Notification

def create_notification(user_id, message):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()