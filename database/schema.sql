-- Create the 'users' table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL
);

-- Create the 'events' table
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(140) NOT NULL,
    description TEXT NOT NULL,
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME NOT NULL,
    location VARCHAR(140) NOT NULL,
    organizer_id INTEGER NOT NULL,
    vendor_id INTEGER,
    FOREIGN KEY (organizer_id) REFERENCES users(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);

-- Create the 'rsvps' table
CREATE TABLE rsvps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    status VARCHAR(64),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Create the 'vendors' table
CREATE TABLE vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(140) NOT NULL,
    service VARCHAR(140) NOT NULL,
    contact_info VARCHAR(140) NOT NULL,
    contract_details TEXT NOT NULL,
    payment_status VARCHAR(64) NOT NULL,
    reviews TEXT,
    organizer_id INTEGER,
    FOREIGN KEY (organizer_id) REFERENCES users(id)
);

-- Create the 'payments' table
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount FLOAT NOT NULL,
    status VARCHAR(64) NOT NULL,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Create the 'event_vendor' association table
CREATE TABLE event_vendor (
    event_id INTEGER NOT NULL,
    vendor_id INTEGER NOT NULL,
    PRIMARY KEY (event_id, vendor_id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);