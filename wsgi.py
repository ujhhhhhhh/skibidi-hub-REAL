#!/usr/bin/env python3
"""
WSGI entry point for Skibidi Hub on Vercel
"""
import os
from main import app

# Set production environment
os.environ.setdefault('FLASK_ENV', 'production')

# Ensure session secret is set
if not os.environ.get('SESSION_SECRET'):
    os.environ['SESSION_SECRET'] = 'skibidi-sigma-ohio-rizz-secret-key-2025'

# WSGI application
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)