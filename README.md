# EventSync Application

EventSync is a web application designed to facilitate event management. It provides tools for organizing events, tracking RSVPs, and managing user interactions. This guide will help you set up and run the EventSync application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:
- [Python](https://www.python.org/downloads/) (version 3.8 or higher)
- [Git](https://git-scm.com/downloads)

## Installation

Follow these steps to get your development environment set up:

1. **Clone the repository**
   ```bash
   git clone https://github.com/leahmirch/CIS376-Event-Sync
   cd CIS376-Event-Sync
   ```

2. **Set up a virtual environment** (optional, but recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On MacOS/Linux
   source venv/bin/activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   flask db upgrade
   flask shell
   >>> from init_db import initialize_database
   >>> initialize_database()
   ```

5. **Seed the database** (Optional):
   ```bash
   sqlite3 app.db < seed.sql
   ```

## Running the Application

1. **Environment Variables**:
   Set environment variables necessary for the application:
   ```bash
   export FLASK_APP=eventsync_app.py
   export FLASK_ENV=development  # Set to 'production' in a production environment
   export SECRET_KEY='your_secret_key_here'
   ```

2. **Start the Flask application**:
   ```bash
   flask run
   ```
   This command will start the server on http://127.0.0.1:5000/.

## Usage

Once the application is running, you can access it via your web browser at `http://127.0.0.1:5000/`. Use the navigation bar to access different sections of the application such as the Dashboard, Login, and Event Management pages.

## Testing

To run tests, use the following command:
```bash
python -m unittest discover
```

## Contact

Leah Mirch - [lmirch@umich.edu](mailto:lmirch@umich.edu)
GitHub: [https://github.com/leahmirch](https://github.com/leahmirch)

## Acknowledgments

- Bootstrap for the CSS framework
- Flask for the web framework
- SQLite for the database
