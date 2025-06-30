import os
import uuid
import logging
import math
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
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB
TEXT_MAX_LENGTH = 2048  # 2KB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'mp3', 'wav', 'doc', 'docx', 'zip'}
POSTS_PER_PAGE = 10  # Pagination
COMMENTS_PER_PAGE = 5  # Comments pagination

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory virtual storage - all data stored in Python dictionaries/lists
VIRTUAL_STORAGE = {
    'posts': [],
    'comments': {},  # post_id -> list of comments
    'likes': {},     # post_id -> list of usernames who liked
    'hall_of_fame': [],
    'hall_of_shame': []
}

# Counter for generating unique post IDs
POST_ID_COUNTER = 1

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Virtual storage access functions
def get_posts():
    """Get all posts from virtual storage"""
    posts = VIRTUAL_STORAGE['posts']
    # Sort by timestamp (newest first)
    return sorted(posts, key=lambda x: x.get('timestamp', ''), reverse=True)

def get_all_comments():
    """Get all comments from virtual storage"""
    return VIRTUAL_STORAGE['comments']

def get_likes():
    """Get all likes from virtual storage"""
    return VIRTUAL_STORAGE['likes']

def get_hall_of_fame():
    """Get hall of fame posts from virtual storage"""
    return VIRTUAL_STORAGE['hall_of_fame']

def get_hall_of_shame():
    """Get hall of shame posts from virtual storage"""
    return VIRTUAL_STORAGE['hall_of_shame']

def save_posts(posts):
    """Save posts to virtual storage"""
    VIRTUAL_STORAGE['posts'] = posts

def save_comments(comments):
    """Save comments to virtual storage"""
    VIRTUAL_STORAGE['comments'] = comments

def get_comments():
    """Get all comments from virtual storage - compatibility function"""
    return VIRTUAL_STORAGE['comments']

def save_likes(likes):
    """Save likes to virtual storage"""
    VIRTUAL_STORAGE['likes'] = likes

def save_hall_of_fame(hall_posts):
    """Save hall of fame to virtual storage"""
    VIRTUAL_STORAGE['hall_of_fame'] = hall_posts

def save_hall_of_shame(hall_posts):
    """Save hall of shame to virtual storage"""
    VIRTUAL_STORAGE['hall_of_shame'] = hall_posts

# Compatibility functions for existing code
load_posts = get_posts
load_comments = get_comments
load_likes = get_likes
load_hall_of_fame = get_hall_of_fame
load_hall_of_shame = get_hall_of_shame

def create_post(username, content, filename=None):
    """Create a new post"""
    global POST_ID_COUNTER
    
    posts = VIRTUAL_STORAGE['posts']  # Get directly to avoid sorting
    post = {
        'id': POST_ID_COUNTER,
        'username': username,
        'content': content,
        'filename': filename,
        'timestamp': datetime.now().isoformat(),
        'skibidi_level': 'sigma'
    }
    posts.append(post)
    
    POST_ID_COUNTER += 1
    return post['id']

def add_comment(post_id, username, comment_content):
    """Add a comment to a post"""
    comments = get_comments()
    
    if str(post_id) not in comments:
        comments[str(post_id)] = []
    
    comment = {
        'id': len(comments[str(post_id)]) + 1,
        'username': username,
        'content': comment_content,
        'timestamp': datetime.now().isoformat()
    }
    
    comments[str(post_id)].append(comment)
    save_comments(comments)
    return comment

def toggle_like(post_id, username):
    """Toggle like for a post by username"""
    likes = get_likes()
    post_id_str = str(post_id)
    
    if post_id_str not in likes:
        likes[post_id_str] = []
    
    if username in likes[post_id_str]:
        likes[post_id_str].remove(username)
        liked = False
    else:
        likes[post_id_str].append(username)
        liked = True
    
    save_likes(likes)
    return liked, len(likes[post_id_str])

def search_posts(query):
    """Search posts by content and username"""
    posts = get_posts()
    if not query:
        return posts
    
    query_lower = query.lower()
    return [post for post in posts 
            if query_lower in post['content'].lower() or 
               query_lower in post['username'].lower()]

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
    flash('File too large! Maximum size is 25MB.', 'danger')
    return redirect(url_for('create_post_route'))

@app.route('/')
def index():
    """Main community feed with pagination and search"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str)
    
    if search_query:
        posts = search_posts(search_query)
    else:
        posts = load_posts()
    
    # Sort posts by timestamp (newest first)
    posts = sorted(posts, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Paginate posts
    pagination = paginate_posts(posts, page, POSTS_PER_PAGE)
    
    # Get comments and likes for each post
    comments_data = load_comments()
    likes_data = load_likes()
    
    for post in pagination['posts']:
        post_id = str(post['id'])
        post['comments_count'] = len(comments_data.get(post_id, []))
        post['likes_count'] = len(likes_data.get(post_id, []))
        post['like_count'] = len(likes_data.get(post_id, []))
        post['comment_count'] = len(comments_data.get(post_id, []))
        
        # Add comments data for the template
        post_comments = comments_data.get(post_id, [])
        post_comments_sorted = sorted(post_comments, key=lambda x: x.get('timestamp', ''), reverse=True)
        post['comments_data'] = post_comments_sorted
    
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
        
        if not username or not content:
            flash('Username and content are required!', 'danger')
            return render_template('create_post.html')
        
        if len(content) > TEXT_MAX_LENGTH:
            flash(f'Content too long! Maximum {TEXT_MAX_LENGTH} characters allowed.', 'danger')
            return render_template('create_post.html')
        
        filename = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        post_id = create_post(username, content, filename)
        flash(f'Skibidi post created! ID: {post_id}', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_post.html')

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    """Toggle like for a post"""
    username = request.form.get('username', '').strip()
    if not username:
        flash('Username required to like!', 'danger')
        return redirect(url_for('index'))
    
    try:
        liked, total_likes = toggle_like(post_id, username)
        action = 'liked' if liked else 'unliked'
        flash(f'Post {action}! Total likes: {total_likes}', 'success')
    except Exception as e:
        logging.error(f"Error toggling like: {e}")
        flash('Error processing like!', 'danger')
    
    return redirect(url_for('index'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment_route(post_id):
    """Add comment to a post"""
    username = request.form.get('username', '').strip()
    comment_content = request.form.get('comment', '').strip()
    
    if not username or not comment_content:
        flash('Username and comment are required!', 'danger')
        return redirect(url_for('index'))
    
    if len(comment_content) > 500:
        flash('Comment too long! Maximum 500 characters.', 'danger')
        return redirect(url_for('index'))
    
    try:
        add_comment(post_id, username, comment_content)
        flash('Comment added!', 'success')
    except Exception as e:
        logging.error(f"Error adding comment: {e}")
        flash('Error adding comment!', 'danger')
    
    return redirect(url_for('index'))

@app.route('/hall-of-fame')
def hall_of_fame():
    """Hall of Fame page"""
    hall_posts = load_hall_of_fame()
    return render_template('hall_of_fame.html', posts=hall_posts)

@app.route('/hall-of-shame')
def hall_of_shame():
    """Hall of Shame page"""
    hall_posts = load_hall_of_shame()
    return render_template('hall_of_shame.html', posts=hall_posts)

@app.route('/api/comments/<int:post_id>')
def get_comments_api(post_id):
    """Get paginated comments for a post"""
    page = request.args.get('page', 1, type=int)
    comments_data = load_comments()
    post_comments = comments_data.get(str(post_id), [])
    
    # Sort comments by timestamp (newest first)
    post_comments = sorted(post_comments, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    pagination = paginate_comments(post_comments, page, COMMENTS_PER_PAGE)
    
    return jsonify({
        'comments': pagination['comments'],
        'has_next': pagination['has_next'],
        'has_prev': pagination['has_prev'],
        'next_num': pagination['next_num'],
        'prev_num': pagination['prev_num'],
        'page': pagination['page'],
        'total_pages': pagination['total_pages'],
        'pagination': pagination
    })

@app.route('/comments/<int:post_id>')
def get_comments_route(post_id):
    """Alternative route for comments (for JavaScript fetch)"""
    return get_comments_api(post_id)

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
    app.run(debug=True)