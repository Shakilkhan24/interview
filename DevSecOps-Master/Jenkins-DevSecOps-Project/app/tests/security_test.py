"""
Security Tests for DevSecOps Application
"""

import pytest
from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sql_injection_protection(client):
    """Test SQL injection protection"""
    # Attempt SQL injection
    response = client.get('/api/v1/users?id=1 OR 1=1',
                         headers={'X-API-Key': 'dev-key-change-in-production'})
    # Should not expose database errors
    assert response.status_code != 500

def test_xss_protection(client):
    """Test XSS protection"""
    xss_payload = '<script>alert("xss")</script>'
    response = client.post('/api/v1/users',
                          headers={'X-API-Key': 'dev-key-change-in-production'},
                          json={'name': xss_payload, 'email': 'test@example.com'})
    # Should sanitize input
    response_data = str(response.data)
    assert '<script>' not in response_data.lower()

def test_authentication_required(client):
    """Test that authentication is required"""
    response = client.get('/api/v1/users')
    assert response.status_code == 401

def test_input_validation(client):
    """Test input validation"""
    # Test empty input
    response = client.post('/api/v1/users',
                          headers={'X-API-Key': 'dev-key-change-in-production'},
                          json={})
    assert response.status_code == 400
    
    # Test invalid email
    response = client.post('/api/v1/users',
                          headers={'X-API-Key': 'dev-key-change-in-production'},
                          json={'name': 'Test', 'email': 'invalid-email'})
    assert response.status_code == 400

def test_input_length_limits(client):
    """Test input length limits"""
    long_string = 'a' * 200
    response = client.post('/api/v1/users',
                          headers={'X-API-Key': 'dev-key-change-in-production'},
                          json={'name': long_string, 'email': 'test@example.com'})
    # Should truncate or reject
    assert response.status_code in [201, 400]

def test_path_traversal_protection(client):
    """Test path traversal protection"""
    # Attempt path traversal
    response = client.get('/api/v1/users?file=../../etc/passwd')
    # Should not expose file system
    assert response.status_code != 200 or 'passwd' not in str(response.data)

