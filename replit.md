# Skibidi Hub

## Overview

This is a Flask-based community hub application themed around internet memes and "brainrot" culture. It's a social media-style platform where users can create posts with text content and file uploads, displaying them in a chronological feed with full social interaction features. The application uses a simple JSON file-based storage system for posts, comments, likes, and special halls of fame/shame content. Features include pagination, search functionality, like/comment systems, and owner-curated hall of fame/shame sections.

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
- **Primary Storage**: JSON file-based system with multiple data files:
  - `data/posts.json` - Main posts content and metadata
  - `data/comments.json` - User comments organized by post ID
  - `data/likes.json` - Like counts and user tracking by post ID
  - `data/hall_of_fame.json` - Owner-curated legendary posts
  - `data/hall_of_shame.json` - Owner-curated shameful posts
- **File Storage**: Local filesystem storage in `uploads/` directory
- **No Database**: Uses file-based storage for simplicity and direct control

## Key Components

### Core Application (`app.py`)
- Flask application setup with configuration
- File upload handling with size and type restrictions
- JSON-based post management system with comments and likes
- Search functionality across posts and usernames
- Pagination system for efficient content browsing
- Like/unlike toggle system with user tracking
- Comment system with character limits
- Hall of Fame/Shame owner-only curation system
- Security features including filename sanitization

### Entry Point (`main.py`)
- Application runner with debug mode enabled
- Configured for development with host binding to 0.0.0.0

### Frontend Templates
- **Base Template**: Common layout with header, navigation, and hall links
- **Index Template**: Main feed with pagination, search, comments, and likes
- **Create Post Template**: Form for creating new posts with file uploads
- **Hall of Fame Template**: Showcase for legendary community posts
- **Hall of Shame Template**: Display for posts deemed inappropriate

### Static Assets
- **CSS**: Enhanced theming with interactive elements, pagination, and hall styling
- **JavaScript**: Advanced interactions for comments, likes, search highlighting, and form management

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

### Vercel Deployment
- **vercel.json**: Configured for Python runtime with @vercel/python
- **wsgi.py**: WSGI entry point for production deployment
- **install.sh**: Dependency installation script for manual deployments
- **build.sh**: Application startup script with Gunicorn configuration
- **dependencies.txt**: Python package requirements list
- **README.md**: Complete deployment guide for Vercel and manual installation

### File System Requirements
- Write permissions for `uploads/` and `data/` directories
- Sufficient storage for user-uploaded files
- JSON file persistence for post data

### Scaling Considerations
- Current architecture suitable for small to medium communities
- File-based storage may need migration to database for larger scale
- Static file serving may need CDN or dedicated file server for production
- Vercel deployment provides automatic scaling and CDN distribution

## Changelog

- June 30, 2025. Initial setup with basic post creation and feed display
- June 30, 2025. Added comprehensive social features:
  - Comments system with 500-byte limit per comment
  - Like/unlike system with user tracking
  - Search functionality across post content and usernames
  - Pagination system (10 posts per page)
  - Hall of Fame for legendary posts (owner-curated)
  - Hall of Shame for inappropriate posts (owner-curated)
  - Enhanced UI with interactive buttons and forms
  - Search result highlighting
  - Mobile-responsive design improvements
- June 30, 2025. Enhanced comment system:
  - Comments are now collapsible by default (hidden until clicked)
  - Added pagination for comments (5 comments per page)
  - AJAX loading for comments with smooth animations
  - Individual comment pagination controls per post
  - Improved mobile responsiveness for comment interactions
- June 30, 2025. Discord integration and rebranding:
  - Rebranded from "Skibidi Toilet Community Hub" to "Skibidi Hub"
  - Added Discord server promotion popup on home page
  - Smart popup system with 15-minute cooldown using localStorage
  - Discord popup only appears on home page with animated design
  - Direct link to Discord server: https://discord.gg/9TN4VvEhH9
- June 30, 2025. Vercel deployment preparation:
  - Created install.sh script for dependency installation
  - Created build.sh script for starting Flask app with Gunicorn
  - Added vercel.json configuration for Vercel Python runtime
  - Created wsgi.py entry point for production deployment
  - Added dependencies.txt with exact package versions
  - Created comprehensive README.md with deployment instructions

## User Preferences

Preferred communication style: Simple, everyday language.