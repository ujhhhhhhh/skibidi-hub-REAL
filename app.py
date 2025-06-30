import os
import json
import uuid
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "skibidi_sigma_ohio_rizz_2024")

# Configuration
UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB
TEXT_MAX_LENGTH = 2048  # 2KB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'mp3', 'wav', 'doc', 'docx', 'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_posts_file():
    """Get path to posts JSON file"""
    return os.path.join(DATA_FOLDER, 'posts.json')

def load_posts():
    """Load all posts from JSON file"""
    posts_file = get_posts_file()
    if os.path.exists(posts_file):
        try:
            with open(posts_file, 'r', encoding='utf-8') as f:
                posts = json.load(f)
                # Sort by timestamp descending (newest first)
                return sorted(posts, key=lambda x: x.get('timestamp', ''), reverse=True)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading posts: {e}")
            return []
    return []

def save_posts(posts):
    """Save posts to JSON file"""
    posts_file = get_posts_file()
    try:
        with open(posts_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        logging.error(f"Error saving posts: {e}")
        return False

def create_post(username, content, filename=None):
    """Create a new post"""
    post = {
        'id': str(uuid.uuid4()),
        'username': username,
        'content': content,
        'filename': filename,
        'timestamp': datetime.now().isoformat(),
        'skibidi_level': 'sigma'  # Default brainrot level
    }
    
    posts = load_posts()
    posts.append(post)
    
    if save_posts(posts):
        return post
    return None

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle file too large error"""
    flash('Yo fam, that file is way too chonky! Keep it under 25MB for maximum Ohio rizz! 🚽', 'error')
    return redirect(url_for('create_post'))

@app.route('/')
def index():
    """Main community feed"""
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post_route():
    """Create new post"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        content = request.form.get('content', '').strip()
        
        # Validate inputs
        if not username:
            flash('Bruh, you gotta drop your Skibidi username! No cap! 🚽', 'error')
            return render_template('create_post.html')
        
        if not content:
            flash('Yo, you forgot the Skibidi content! Drop some brainrot wisdom! 📸', 'error')
            return render_template('create_post.html')
        
        if len(content.encode('utf-8')) > TEXT_MAX_LENGTH:
            flash(f'That post is too long, fam! Keep it under {TEXT_MAX_LENGTH} bytes for maximum sigma energy! ⚡', 'error')
            return render_template('create_post.html')
        
        # Handle file upload
        uploaded_filename = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    # Generate unique filename
                    file_extension = secure_filename(file.filename).rsplit('.', 1)[1].lower()
                    unique_filename = f"{uuid.uuid4()}.{file_extension}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    
                    try:
                        file.save(file_path)
                        uploaded_filename = unique_filename
                        logging.info(f"File saved: {file_path}")
                    except Exception as e:
                        logging.error(f"Error saving file: {e}")
                        flash('Failed to upload your Skibidi content! Try again, sigma! 💀', 'error')
                        return render_template('create_post.html')
                else:
                    flash('That file type is sus! Only upload valid Skibidi formats! 📁', 'error')
                    return render_template('create_post.html')
        
        # Create the post
        post = create_post(username, content, uploaded_filename)
        if post:
            flash('Skibidi post created successfully! You\'re absolutely sigma! 🚽✨', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to create your Skibidi post! The toilet gods are angry! 😱', 'error')
    
    return render_template('create_post.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/posts')
def api_posts():
    """API endpoint for posts (if needed for AJAX)"""
    posts = load_posts()
    return jsonify(posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
