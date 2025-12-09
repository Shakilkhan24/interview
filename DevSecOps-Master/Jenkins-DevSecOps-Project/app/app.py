#!/usr/bin/env python3
"""
DevSecOps Sample Application
Secure Python Flask Application
"""

from flask import Flask, jsonify, request
import os
import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Security headers
@app.after_request
def set_security_headers(response):
    """Set security headers for all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('API_KEY', 'dev-key-change-in-production')
        
        if not api_key or api_key != expected_key:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'devsecops-app'
    }), 200

@app.route('/api/v1/users', methods=['GET'])
@require_api_key
def get_users():
    """Get users endpoint (protected)"""
    # Simulated user data
    users = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
    ]
    return jsonify(users), 200

@app.route('/api/v1/users', methods=['POST'])
@require_api_key
def create_user():
    """Create user endpoint (protected)"""
    data = request.get_json()
    
    # Input validation
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    # Sanitize input (basic example)
    name = data['name'][:100]  # Limit length
    email = data['email'][:100]
    
    # Validate email format (basic)
    if '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 400
    
    logger.info(f"Creating user: {name} ({email})")
    
    return jsonify({
        'id': 3,
        'name': name,
        'email': email
    }), 201

@app.route('/api/v1/info', methods=['GET'])
def info():
    """Application info endpoint"""
    return jsonify({
        'name': 'DevSecOps Application',
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'environment': os.getenv('NODE_ENV', 'development')
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Security: Don't run in debug mode in production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    
    app.run(host=host, port=port, debug=debug_mode)

