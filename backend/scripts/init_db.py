import sqlite3
import os

def initialize_database():
    # Define the path to your schema SQL file
    schema_path = 'schema.sql'
    
    # Connect to the SQLite database (this will create the database file if it does not exist)
    db_path = os.path.join(os.getcwd(), 'eventsync.db')
    conn = sqlite3.connect(db_path)
    
    # Open the schema file and read its contents
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Execute the schema script
    conn.executescript(schema)
    print("Database initialized with the following schema:")
    print(schema)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
