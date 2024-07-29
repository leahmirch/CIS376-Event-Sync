-- Schema.sql
-- SQL commands to create the necessary tables for the EventSync application

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
    description TEXT,
    date DATETIME,
    location VARCHAR(140),
    organizer_id INTEGER,
    FOREIGN KEY (organizer_id) REFERENCES users(id)
);

-- Create the 'rsvps' table
CREATE TABLE rsvps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_id INTEGER,
    status VARCHAR(64),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Indexes to improve query performance
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_event_organizer ON events(organizer_id);
