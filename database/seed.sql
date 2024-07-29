-- Insert initial user data
INSERT INTO users (username, email, password_hash) VALUES
('admin', 'admin@example.com', 'hashed_admin_password'),
('organizer', 'organizer@example.com', 'hashed_organizer_password');

-- Insert initial event data
INSERT INTO events (name, description, date, location, organizer_id) VALUES
('Annual Tech Conference', 'A comprehensive gathering for technology enthusiasts and professionals.', '2023-10-15 09:00', 'Convention Center, City', 1),
('Local Music Festival', 'Celebrating local music talents and cultural festivities.', '2023-08-21 12:00', 'Downtown Park, City', 2);

-- Insert initial RSVP data
INSERT INTO rsvps (user_id, event_id, status) VALUES
(1, 1, 'Accepted'),
(2, 1, 'Pending'),
(1, 2, 'Declined');
