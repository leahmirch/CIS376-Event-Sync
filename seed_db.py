from werkzeug.security import generate_password_hash
from backend.models import db, User, Event, Vendor
from datetime import datetime

def add_user_to_db(username, email, password):
    user = User(username=username, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

def add_event_to_db(name, description, start_datetime, end_datetime, location, organizer_id):
    event = Event(
        name=name,
        description=description,
        start_datetime=datetime.strptime(start_datetime, '%Y-%m-%d %H:%M'),
        end_datetime=datetime.strptime(end_datetime, '%Y-%m-%d %H:%M'),
        location=location,
        organizer_id=organizer_id
    )
    db.session.add(event)
    db.session.commit()

def add_vendor_to_db(name, contact_info, contract_details):
    vendor = Vendor(name=name, contact_info=contact_info, contract_details=contract_details)
    db.session.add(vendor)
    db.session.commit()

if __name__ == "__main__":
    from eventsync_app import app

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Adding initial users
        add_user_to_db('admin', 'admin@example.com', 'password')
        add_user_to_db('organizer', 'organizer@example.com', 'password')

        # Adding initial vendors
        add_vendor_to_db('Vendor A', 'contact@vendora.com', 'Contract details for Vendor A')
        add_vendor_to_db('Vendor B', 'contact@vendorb.com', 'Contract details for Vendor B')

        # Adding initial events
        add_event_to_db(
            'Annual Tech Conference', 'A comprehensive gathering for technology enthusiasts and professionals.',
            '2023-10-15 09:00', '2023-10-15 17:00',
            'Convention Center, City', 1
        )
        add_event_to_db(
            'Local Music Festival', 'Celebrating local music talents and cultural festivities.',
            '2023-08-21 12:00', '2023-08-21 22:00',
            'Downtown Park, City', 2
        )

        print("Database seeded successfully.")
