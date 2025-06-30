# Skibidi Toilet Community Hub

## Overview

This is a Flask-based community hub application themed around internet memes and "brainrot" culture. It's a social media-style platform where users can create posts with text content and file uploads, displaying them in a chronological feed. The application uses a simple JSON file-based storage system for posts and includes a file upload system for media attachments.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap 5 for responsive design
- **Custom Styling**: Themed CSS with meme-inspired design elements
- **JavaScript**: Vanilla JavaScript for interactive features and file upload enhancements
- **Icons**: Font Awesome for UI icons

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **File Structure**: Simple MVC pattern with templates, static files, and main application logic
- **Session Management**: Flask sessions with configurable secret key
- **Error Handling**: Basic exception handling with user-friendly flash messages

### Data Storage
- **Primary Storage**: JSON file-based system (`data/posts.json`)
- **File Storage**: Local filesystem storage in `uploads/` directory
- **No Database**: Currently uses file-based storage without traditional database

## Key Components

### Core Application (`app.py`)
- Flask application setup with configuration
- File upload handling with size and type restrictions
- JSON-based post management system
- Security features including filename sanitization

### Entry Point (`main.py`)
- Application runner with debug mode enabled
- Configured for development with host binding to 0.0.0.0

### Frontend Templates
- **Base Template**: Common layout with header, navigation, and styling
- **Index Template**: Main feed displaying posts chronologically
- **Create Post Template**: Form for creating new posts with file uploads

### Static Assets
- **CSS**: Custom theming with CSS variables and responsive design
- **JavaScript**: Interactive features for file uploads and UI enhancements

## Data Flow

1. **Post Creation**: Users submit form data (username, content, optional file)
2. **File Processing**: Uploaded files are validated, renamed securely, and stored
3. **Data Persistence**: Post metadata stored in JSON file with timestamp and unique ID
4. **Feed Display**: Posts loaded from JSON, sorted by timestamp (newest first)
5. **File Serving**: Static files served from uploads directory

## External Dependencies

### Python Packages
- **Flask**: Web framework and templating
- **Werkzeug**: File upload utilities and security features

### Frontend Libraries
- **Bootstrap 5**: CSS framework via CDN
- **Font Awesome**: Icon library via CDN

### File Upload Constraints
- **Maximum Size**: 25MB per file
- **Text Limit**: 2KB for post content
- **Allowed Extensions**: txt, pdf, png, jpg, jpeg, gif, mp4, webm, mp3, wav, doc, docx, zip

## Deployment Strategy

### Current Configuration
- **Development Mode**: Debug enabled, runs on port 5000
- **Host Binding**: 0.0.0.0 for container compatibility
- **Environment Variables**: Session secret configurable via SESSION_SECRET

### File System Requirements
- Write permissions for `uploads/` and `data/` directories
- Sufficient storage for user-uploaded files
- JSON file persistence for post data

### Scaling Considerations
- Current architecture suitable for small to medium communities
- File-based storage may need migration to database for larger scale
- Static file serving may need CDN or dedicated file server for production

## Changelog

- June 30, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.