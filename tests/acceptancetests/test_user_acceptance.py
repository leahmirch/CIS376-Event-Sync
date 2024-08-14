import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="module")
def session():
    with requests.Session() as session:
        yield session

def test_user_login(session):
    # Ensure the user is created before testing login
    signup_url = f"{BASE_URL}/register"
    signup_data = {
        "username": "newuser",
        "password": "password123",
        "email": "newuser@example.com"
    }
    session.post(signup_url, data=signup_data)
    
    # Test user login
    login_url = f"{BASE_URL}/login"
    data = {
        "username": "newuser",
        "password": "password123"
    }
    response = session.post(login_url, data=data)
    
    assert response.status_code == 200

def test_accept_event_invitation(session):
    # Test accepting an event invitation
    event_id = 1  # Replace with the actual event ID to test
    accept_url = f"{BASE_URL}/accept_success/{event_id}"
    response = session.get(accept_url)
    assert response.status_code == 200
    assert "You have successfully accepted the invitation" in response.text

def test_decline_event_invitation(session):
    # Test declining an event invitation
    event_id = 1  # Replace with the actual event ID to test
    decline_url = f"{BASE_URL}/decline_success/{event_id}"
    response = session.get(decline_url)
    assert response.status_code == 200
    assert "You have successfully declined the invitation" in response.text
