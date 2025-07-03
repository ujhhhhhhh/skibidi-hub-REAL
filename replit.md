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
- **Primary Storage**: In-memory Python dictionaries for fast data access:
  - JSON data files: posts, comments, likes, hall_of_fame, hall_of_shame, videos
  - Real-time data storage with instant read/write operations
  - Automatic backup system to external URLs (configurable via BACKUP_URL)
- **File Storage**: In-memory base64 encoded file storage
  - Files stored as base64 strings in memory alongside metadata
  - Virtual file serving through Flask Response objects
  - Supports all file types including images, videos, documents
- **Backup System**: Periodic data backups sent to external URL:
  - Configurable backup interval via BACKUP_INTERVAL environment variable
  - JSON payload with timestamp and all application data
  - One-way backup system (send only, no retrieval)

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

### File Upload Constraints (Vercel Optimized)
- **Maximum File Size**: 2.5MB per file (Vercel 3MB payload limit compliance)
- **Text Limit**: 2KB for post content
- **Comment Limit**: 500 bytes per comment
- **Username Limit**: 50 characters
- **Total Request Limit**: 3MB (enforced via payload validation)
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
- June 30, 2025. Vercel Blob Storage integration and Replit migration:
  - Fully integrated Vercel Blob Storage for all data persistence
  - Migrated from local JSON files to cloud-based blob storage
  - Updated file upload system to use blob storage with direct URLs
  - Automatic data migration from local files to cloud storage
  - Enhanced file serving with blob URL redirects and local fallback
  - Completed migration from Replit Agent to standard Replit environment
- June 30, 2025. Critical frontend bug fixes and data reset:
  - Fixed JavaScript function scoping issue preventing like/comment button functionality
  - Exposed functions globally via window object for onclick handlers
  - Resolved file path double-prefix bug in storage service
  - Added comprehensive error handling and loading states
  - Successfully reset all data (posts, comments, likes) for fresh user testing
  - Application now fully functional with all social features working
- June 30, 2025. File storage system optimization:
  - Fixed file upload/serving to use Vercel Blob Storage exclusively
  - Removed local file fallbacks to ensure cloud-only file operations
  - Updated file paths to eliminate double "uploads/" prefix issues
  - Files now upload directly to blob storage and serve via redirect to blob URLs
  - Verified end-to-end file upload and serving functionality
- July 3, 2025. Replit Agent to Replit migration:
  - Successfully migrated project from Replit Agent to standard Replit environment
  - Added maintenance mode feature triggered by MAINTENANCE_MODE environment variable
  - Created beautiful maintenance page with animated design and Discord link
  - Maintained all existing functionality and security practices
  - Server running on gunicorn with proper Flask configuration
- July 3, 2025. Storage system migration to in-memory with backup:
  - Migrated from Vercel Blob Storage to in-memory Python dictionaries
  - Implemented automatic backup system with configurable external URL
  - Added periodic backup thread with configurable intervals
  - Updated file handling to use in-memory base64 encoded storage
  - Files stored virtually as base64 strings with metadata (content type, size, timestamp)
  - Virtual file serving through Flask Response objects for Vercel compatibility
  - Backup system sends JSON data to BACKUP_URL without retrieval functionality
  - Enhanced performance with instant in-memory data operations
  - Completely virtual filesystem - no local file dependencies
- July 3, 2025. Vercel payload compliance implementation:
  - Implemented comprehensive 3MB payload limit validation for all endpoints
  - Reduced maximum file size from 25MB to 2.5MB to ensure Vercel compatibility
  - Added payload size validation functions for create posts, comments, and video uploads
  - Updated all frontend templates to display new 2.5MB file size limits
  - Added request size calculation before processing any uploads
  - Enhanced backup system with payload size monitoring and warnings
  - Updated JavaScript validation to enforce 2.5MB limits client-side
  - All user actions now validated against Vercel's 3MB request limit

## User Preferences

Preferred communication style: Simple, everyday language.