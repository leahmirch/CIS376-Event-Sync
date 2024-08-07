from werkzeug.security import generate_password_hash
from backend.models import db, User, Event, Vendor, RSVP
from datetime import datetime

def add_user_to_db(username, email, password):
    user = User(username=username, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user.id

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
    return event.id

def add_vendor_to_db(name, contact_info, contract_details):
    vendor = Vendor(name=name, contact_info=contact_info, contract_details=contract_details)
    db.session.add(vendor)
    db.session.commit()

def add_rsvp_to_db(user_id, event_id, status):
    rsvp = RSVP(user_id=user_id, event_id=event_id, status=status)
    db.session.add(rsvp)
    db.session.commit()

if __name__ == "__main__":
    from eventsync_app import app

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Adding initial users
        admin_id = add_user_to_db('admin', 'admin@example.com', 'password')
        john_id = add_user_to_db('john_doe', 'john.doe@example.com', 'password')
        jane_id = add_user_to_db('jane_smith', 'jane.smith@example.com', 'password')
        emily_id = add_user_to_db('emily_jones', 'emily.jones@example.com', 'password')
        michael_id = add_user_to_db('michael_brown', 'michael.brown@example.com', 'password')
        organizer_id = add_user_to_db('organizer', 'organizer@example.com', 'password')

        # Adding initial vendors
        add_vendor_to_db('Tech Solutions', 'contact@techsolutions.com', 'Contract for tech equipment and services.')
        add_vendor_to_db('Catering Co.', 'info@cateringco.com', 'Contract for event catering services.')
        add_vendor_to_db('Event Decor', 'sales@eventdecor.com', 'Contract for event decoration and setup.')
        add_vendor_to_db('Sound and Light', 'support@soundandlight.com', 'Contract for sound and lighting services.')
        add_vendor_to_db('Venue Rentals', 'contact@venuerentals.com', 'Contract for venue rentals.')

        # Adding initial events
        tech_conference_id = add_event_to_db(
            'Annual Tech Conference', 'A comprehensive gathering for technology enthusiasts and professionals.',
            '2023-10-15 09:00', '2023-10-15 17:00',
            'Convention Center, City', admin_id
        )
        music_festival_id = add_event_to_db(
            'Local Music Festival', 'Celebrating local music talents and cultural festivities.',
            '2023-08-21 12:00', '2023-08-21 22:00',
            'Downtown Park, City', john_id
        )
        pitch_night_id = add_event_to_db(
            'Startup Pitch Night', 'An evening for startups to pitch their ideas to potential investors.',
            '2024-02-10 18:00', '2024-02-10 21:00',
            'Innovation Hub, City', jane_id
        )
        charity_gala_id = add_event_to_db(
            'Charity Gala', 'A formal event to raise funds for local charities.',
            '2024-05-05 19:00', '2024-05-05 23:00',
            'Grand Ballroom, City', emily_id
        )
        art_exhibition_id = add_event_to_db(
            'Art Exhibition', 'Showcasing works of local artists.',
            '2023-07-10 10:00', '2023-07-10 17:00',
            'Art Gallery, City', michael_id
        )
        book_fair_id = add_event_to_db(
            'Book Fair', 'A fair for book lovers to meet authors and buy books.',
            '2024-11-25 09:00', '2024-11-25 18:00',
            'Exhibition Center, City', organizer_id
        )

        # Associating vendors with events
        event1 = Event.query.get(tech_conference_id)
        event2 = Event.query.get(music_festival_id)
        event3 = Event.query.get(pitch_night_id)
        event4 = Event.query.get(charity_gala_id)
        event5 = Event.query.get(art_exhibition_id)
        event6 = Event.query.get(book_fair_id)

        vendor1 = Vendor.query.get(1)
        vendor2 = Vendor.query.get(2)
        vendor3 = Vendor.query.get(3)
        vendor4 = Vendor.query.get(4)
        vendor5 = Vendor.query.get(5)

        event1.vendors.append(vendor1)
        event1.vendors.append(vendor2)
        event2.vendors.append(vendor3)
        event3.vendors.append(vendor4)
        event4.vendors.append(vendor1)
        event4.vendors.append(vendor5)
        event5.vendors.append(vendor2)
        event6.vendors.append(vendor3)
        event6.vendors.append(vendor4)

        db.session.commit()

        # Adding RSVPs
        add_rsvp_to_db(john_id, tech_conference_id, 'Accepted')
        add_rsvp_to_db(jane_id, tech_conference_id, 'Declined')
        add_rsvp_to_db(emily_id, tech_conference_id, 'Pending')
        add_rsvp_to_db(michael_id, music_festival_id, 'Accepted')
        add_rsvp_to_db(admin_id, charity_gala_id, 'Accepted')
        add_rsvp_to_db(john_id, art_exhibition_id, 'Declined')
        add_rsvp_to_db(jane_id, book_fair_id, 'Accepted')
        add_rsvp_to_db(emily_id, book_fair_id, 'Pending')

        add_feedback_to_db(1, 1, 'Great event, learned a lot!', 5)
        add_feedback_to_db(2, 2, 'Loved the music!', 4)

        print("Database seeded successfully.")
