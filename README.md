# EventSync Application

EventSync is a web application designed to facilitate event management. It provides tools for organizing events, tracking RSVPs, and managing user interactions. This guide will help you set up and run the EventSync application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:
- [Python](https://www.python.org/downloads/) (version 3.8 or higher)
- [Git](https://git-scm.com/downloads)
- [SQLite](https://www.sqlite.org/download.html)

## Installation

Follow these steps to get your development environment set up:

### 1. Clone the Repository
```bash
git clone https://github.com/leahmirch/CIS376-Event-Sync.git
cd CIS376-Event-Sync
```

### 2. Set Up SQLite
1. **Download SQLite Tools**:
   - Download the "Precompiled Binaries for Windows" from SQLite:
     [Download SQLite Tools](https://www.sqlite.org/2023/sqlite-tools-win-x64-3460000.zip)

2. **Extract Files**:
   - Extract the contents to `C:\sqlite`. Ensure `sqlite3.exe` is directly inside `C:\sqlite`.

3. **Verify Installation**:
   - Open Git Bash and run:
     ```bash
     /c/sqlite/sqlite3.exe --version
     ```
   - You should see the SQLite version output.

### 3. Set Up a Virtual Environment
```bash
python -m venv venv
# On Windows
source venv/Scripts/activate
# On macOS/Linux
source venv/bin/activate
```

### 4. Install Required Packages
```bash
pip install -r requirements.txt
```

### 5. Initialize the Database
```bash
python backend/scripts/init_db.py
```

### 6. Seed the Database
```bash
/c/sqlite/sqlite3.exe database/eventsync.db < database/seed.sql
```

### 7. Set Environment Variables
Set environment variables necessary for the application:
```bash
export FLASK_APP=eventsync_app.py
export FLASK_ENV=development  # Set to 'production' in a production environment
export SECRET_KEY='your-secret-key-here'
```

### 8. Run the Flask Application
Start the Flask application:
```bash
flask run
```
This command will start the server on `http://127.0.0.1:5000/`.

### Troubleshooting
If you encounter `ERR_CONNECTION_REFUSED`, ensure the following:
- Flask is running and not reporting any errors.
- The firewall is not blocking the connection.
- You are accessing the correct URL: `http://127.0.0.1:5000/`.

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
```