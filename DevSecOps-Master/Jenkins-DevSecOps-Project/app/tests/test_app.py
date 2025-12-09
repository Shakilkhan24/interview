"""
Unit Tests for DevSecOps Application
"""

import pytest
from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_info_endpoint(client):
    """Test info endpoint"""
    response = client.get('/api/v1/info')
    assert response.status_code == 200
    assert 'name' in response.json

def test_get_users_unauthorized(client):
    """Test get users without API key"""
    response = client.get('/api/v1/users')
    assert response.status_code == 401

def test_get_users_authorized(client):
    """Test get users with API key"""
    response = client.get('/api/v1/users', headers={'X-API-Key': 'dev-key-change-in-production'})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_user_invalid_input(client):
    """Test create user with invalid input"""
    response = client.post('/api/v1/users',
                          headers={'X-API-Key': 'dev-key-change-in-production'},
                          json={})
    assert response.status_code == 400

def test_create_user_valid(client):
    """Test create user with valid input"""
    response = client.post('/api/v1/users',
                          headers={'X-API-Key': 'dev-key-change-in-production'},
                          json={'name': 'Test User', 'email': 'test@example.com'})
    assert response.status_code == 201
    assert response.json['name'] == 'Test User'

def test_security_headers(client):
    """Test security headers are present"""
    response = client.get('/health')
    assert 'X-Content-Type-Options' in response.headers
    assert 'X-Frame-Options' in response.headers
    assert 'X-XSS-Protection' in response.headers

