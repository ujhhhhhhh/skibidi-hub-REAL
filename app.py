import os
import json
import uuid
import logging
import math
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify

# Configure logging.
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "skibidi_sigma_ohio_rizz_2024")

# Configuration
UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB
TEXT_MAX_LENGTH = 2048  # 2KB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'mp3', 'wav', 'doc', 'docx', 'zip'}
POSTS_PER_PAGE = 10  # Pagination
COMMENTS_PER_PAGE = 5  # Comments pagination

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

def get_comments_file():
    """Get path to comments JSON file"""
    return os.path.join(DATA_FOLDER, 'comments.json')

def get_likes_file():
    """Get path to likes JSON file"""
    return os.path.join(DATA_FOLDER, 'likes.json')

def get_hall_of_fame_file():
    """Get path to hall of fame JSON file"""
    return os.path.join(DATA_FOLDER, 'hall_of_fame.json')

def get_hall_of_shame_file():
    """Get path to hall of shame JSON file"""
    return os.path.join(DATA_FOLDER, 'hall_of_shame.json')

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

def load_comments():
    """Load all comments from JSON file"""
    comments_file = get_comments_file()
    if os.path.exists(comments_file):
        try:
            with open(comments_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading comments: {e}")
            return {}
    return {}

def load_likes():
    """Load all likes from JSON file"""
    likes_file = get_likes_file()
    if os.path.exists(likes_file):
        try:
            with open(likes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading likes: {e}")
            return {}
    return {}

def load_hall_of_fame():
    """Load hall of fame posts"""
    hall_file = get_hall_of_fame_file()
    if os.path.exists(hall_file):
        try:
            with open(hall_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading hall of fame: {e}")
            return []
    return []

def load_hall_of_shame():
    """Load hall of shame posts"""
    hall_file = get_hall_of_shame_file()
    if os.path.exists(hall_file):
        try:
            with open(hall_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading hall of shame: {e}")
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

def save_comments(comments):
    """Save comments to JSON file"""
    comments_file = get_comments_file()
    try:
        with open(comments_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        logging.error(f"Error saving comments: {e}")
        return False

def save_likes(likes):
    """Save likes to JSON file"""
    likes_file = get_likes_file()
    try:
        with open(likes_file, 'w', encoding='utf-8') as f:
            json.dump(likes, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        logging.error(f"Error saving likes: {e}")
        return False

def create_post(username, content, filename=None):
    """Create a new post"""
    post = {
        'id': str(uuid.uuid4()),
        'username': username,
        'content': content,
        'filename': filename,
        'timestamp': datetime.now().isoformat(),
        'skibidi_level': 'sigma',  # Default brainrot level
        'likes': 0,
        'comments': []
    }
    
    posts = load_posts()
    posts.append(post)
    
    if save_posts(posts):
        return post
    return None

def add_comment(post_id, username, comment_content):
    """Add a comment to a post"""
    comment = {
        'id': str(uuid.uuid4()),
        'username': username,
        'content': comment_content,
        'timestamp': datetime.now().isoformat()
    }
    
    comments = load_comments()
    if post_id not in comments:
        comments[post_id] = []
    comments[post_id].append(comment)
    
    if save_comments(comments):
        return comment
    return None

def toggle_like(post_id, username):
    """Toggle like for a post by username"""
    likes = load_likes()
    if post_id not in likes:
        likes[post_id] = []
    
    if username in likes[post_id]:
        likes[post_id].remove(username)
        action = 'unliked'
    else:
        likes[post_id].append(username)
        action = 'liked'
    
    save_likes(likes)
    return action, len(likes[post_id])

def search_posts(query):
    """Search posts by content and username"""
    posts = load_posts()
    if not query:
        return posts
    
    query_lower = query.lower()
    filtered_posts = []
    
    for post in posts:
        if (query_lower in post.get('content', '').lower() or 
            query_lower in post.get('username', '').lower()):
            filtered_posts.append(post)
    
    return filtered_posts

def paginate_posts(posts, page, per_page):
    """Paginate posts"""
    total = len(posts)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_posts = posts[start:end]
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    return {
        'posts': paginated_posts,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page < total_pages else None
    }

def paginate_comments(comments, page, per_page):
    """Paginate comments for a post"""
    total = len(comments)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_comments = comments[start:end]
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    return {
        'comments': paginated_comments,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page < total_pages else None
    }

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle file too large error"""
    flash('Yo fam, that file is way too chonky! Keep it under 25MB for maximum Ohio rizz! 🚽', 'error')
    return redirect(url_for('create_post'))

@app.route('/')
def index():
    """Main community feed with pagination and search"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str)
    
    # Get posts (filtered by search if query provided)
    if search_query:
        posts = search_posts(search_query)
    else:
        posts = load_posts()
    
    # Add likes and comments data to posts
    likes = load_likes()
    comments = load_comments()
    
    for post in posts:
        post_id = post['id']
        post['like_count'] = len(likes.get(post_id, []))
        post_comments = comments.get(post_id, [])
        post['comment_count'] = len(post_comments)
        
        # Sort comments by timestamp (newest first)
        post_comments_sorted = sorted(post_comments, key=lambda x: x.get('timestamp', ''), reverse=True)
        post['comments_data'] = post_comments_sorted
    
    # Paginate posts
    pagination = paginate_posts(posts, page, POSTS_PER_PAGE)
    
    return render_template('index.html', 
                         posts=pagination['posts'],
                         pagination=pagination,
                         search_query=search_query)

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
            if file.filename and file.filename != '':
                if file and file.filename and allowed_file(file.filename):
                    # Generate unique filename
                    secure_name = secure_filename(file.filename)
                    file_extension = secure_name.rsplit('.', 1)[1].lower()
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

@app.route('/like/<post_id>', methods=['POST'])
def like_post(post_id):
    """Toggle like for a post"""
    username = request.form.get('username', '').strip()
    if not username:
        flash('You need to provide a username to like posts! Drop your Skibidi name! 🚽', 'error')
        return redirect(url_for('index'))
    
    action, like_count = toggle_like(post_id, username)
    
    if action == 'liked':
        flash(f'Sigma energy added! That post is now more rizz! ⚡', 'success')
    else:
        flash(f'Like removed! Still sigma though! 💀', 'success')
    
    return redirect(url_for('index'))

@app.route('/comment/<post_id>', methods=['POST'])
def add_comment_route(post_id):
    """Add comment to a post"""
    username = request.form.get('username', '').strip()
    comment_content = request.form.get('comment', '').strip()
    
    if not username:
        flash('Bruh, drop your username to comment! No anonymous Ohio energy! 🚽', 'error')
        return redirect(url_for('index'))
    
    if not comment_content:
        flash('You gotta write something sigma for your comment! 📸', 'error')
        return redirect(url_for('index'))
    
    if len(comment_content.encode('utf-8')) > 500:  # 500 bytes for comments
        flash('That comment is too long! Keep it under 500 bytes for maximum brainrot! 💀', 'error')
        return redirect(url_for('index'))
    
    comment = add_comment(post_id, username, comment_content)
    if comment:
        flash('Comment added! Your brainrot wisdom has been shared! ⚡', 'success')
    else:
        flash('Failed to add comment! The Skibidi gods are upset! 😱', 'error')
    
    return redirect(url_for('index'))

@app.route('/hall-of-fame')
def hall_of_fame():
    """Hall of Fame page"""
    fame_posts = load_hall_of_fame()
    return render_template('hall_of_fame.html', posts=fame_posts, hall_type='fame')

@app.route('/hall-of-shame')
def hall_of_shame():
    """Hall of Shame page"""
    shame_posts = load_hall_of_shame()
    return render_template('hall_of_shame.html', posts=shame_posts, hall_type='shame')

@app.route('/comments/<post_id>')
def get_comments(post_id):
    """Get paginated comments for a post"""
    page = request.args.get('page', 1, type=int)
    comments = load_comments()
    post_comments = comments.get(post_id, [])
    
    # Sort comments by timestamp (newest first)
    post_comments_sorted = sorted(post_comments, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Paginate comments
    pagination = paginate_comments(post_comments_sorted, page, COMMENTS_PER_PAGE)
    
    return jsonify({
        'comments': pagination['comments'],
        'pagination': {
            'page': pagination['page'],
            'total_pages': pagination['total_pages'],
            'has_prev': pagination['has_prev'],
            'has_next': pagination['has_next'],
            'prev_num': pagination['prev_num'],
            'next_num': pagination['next_num'],
            'total': pagination['total']
        }
    })

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
