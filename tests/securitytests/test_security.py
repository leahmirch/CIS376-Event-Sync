import pytest
import requests

# Base URL of your Flask application
BASE_URL = "http://localhost:5000"

@pytest.fixture
def session():
    """Creates a session for maintaining cookies and other settings."""
    with requests.Session() as s:
        yield s

def test_xss(session):
    """Test for Cross-Site Scripting (XSS) vulnerability."""
    xss_payload = "<script>alert('XSS');</script>"
    response = session.post(f"{BASE_URL}/events", data={"name": xss_payload, "description": "XSS Test", "start_datetime": "2024-08-13T14:00:00", "end_datetime": "2024-08-13T16:00:00", "location": "Test Location", "organizer_id": 1})
    assert xss_payload not in response.text, "Potential XSS vulnerability"

def test_sensitive_data_exposure(session):
    """Test for sensitive data exposure in responses."""
    response = session.get(f"{BASE_URL}/user_profile")
    assert "password" not in response.text, "Sensitive data exposure vulnerability"
