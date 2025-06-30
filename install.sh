#!/bin/bash

# install.sh - Install dependencies for Skibidi Hub on Vercel

echo "Installing Skibidi Hub dependencies..."

# Upgrade pip to latest version
python3 -m pip install --upgrade pip

# Install Python dependencies from dependencies.txt
echo "Installing Flask and required modules..."
if [ -f "dependencies.txt" ]; then
    pip3 install -r dependencies.txt
else
    # Fallback individual installs
    pip3 install flask
    pip3 install flask-sqlalchemy
    pip3 install gunicorn
    pip3 install werkzeug
    pip3 install psycopg2-binary
    pip3 install email-validator
fi

# Create necessary directories
echo "Creating required directories..."
mkdir -p data
mkdir -p uploads
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

# Set proper permissions
chmod 755 data
chmod 755 uploads
chmod +x build.sh

# Create empty data files if they don't exist
touch data/posts.json
touch data/comments.json
touch data/likes.json
touch data/hall_of_fame.json
touch data/hall_of_shame.json

# Initialize empty JSON arrays in data files if they're empty
echo "Initializing data files..."
for file in data/posts.json data/comments.json data/likes.json data/hall_of_fame.json data/hall_of_shame.json; do
    if [ ! -s "$file" ]; then
        echo "[]" > "$file"
    fi
done

echo "✅ Installation complete! Skibidi Hub is ready to deploy!"
echo "🎯 Run ./build.sh to start the application"