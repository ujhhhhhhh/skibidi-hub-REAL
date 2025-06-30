#!/bin/bash

# build.sh - Start Skibidi Hub Flask application with Gunicorn

echo "🚽 Starting Skibidi Hub..."

# Set environment variables for production
export FLASK_ENV=production
export FLASK_APP=main.py

# Set session secret if not provided
if [ -z "$SESSION_SECRET" ]; then
    export SESSION_SECRET="skibidi-sigma-ohio-rizz-secret-key-2025"
    echo "⚠️  Using default session secret. Set SESSION_SECRET environment variable for production."
fi

# Ensure data directory exists and has proper permissions
mkdir -p data uploads
chmod 755 data uploads

# Initialize empty JSON files if they don't exist
for file in data/posts.json data/comments.json data/likes.json data/hall_of_fame.json data/hall_of_shame.json; do
    if [ ! -f "$file" ]; then
        echo "[]" > "$file"
        echo "📁 Created $file"
    fi
done

# Start Gunicorn server
echo "🚀 Starting Gunicorn server on 0.0.0.0:5000..."
echo "📊 Access your Skibidi Hub at the provided URL"

# Use Gunicorn with optimized settings for Vercel
exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 1 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    main:app