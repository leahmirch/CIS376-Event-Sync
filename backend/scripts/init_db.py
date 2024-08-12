import sqlite3
import os

def initialize_database():
    schema_path = os.path.join('database', 'schema.sql')
    db_path = os.path.join(os.getcwd(), 'eventsync.db')
    conn = sqlite3.connect(db_path)
    
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    try:
        conn.executescript(schema)
        print("Database initialized with the following schema:")
        print(schema)
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
