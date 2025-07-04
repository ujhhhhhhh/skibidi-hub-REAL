import os
import json
import uuid
import logging
import math
import sys
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, Response
from memory_storage import memory_storage

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET",
                                "skibidi_sigma_ohio_rizz_2024")
# Configuration - no longer using local file storage
# All files are stored in memory as base64 encoded data

# VERCEL PAYLOAD LIMITS - Critical for deployment
VERCEL_MAX_PAYLOAD = 3 * 1024 * 1024  # 3MB Vercel limit
MAX_CONTENT_LENGTH = 2.5 * 1024 * 1024  # 2.5MB max file size (leave buffer for other data)
TEXT_MAX_LENGTH = 2048  # 2KB max text content
MAX_COMMENT_LENGTH = 500  # 500 bytes max comment
MAX_USERNAME_LENGTH = 50  # 50 chars max username

ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'mp3', 'wav',
    'doc', 'docx', 'zip'
}
VIDEO_EXTENSIONS = {'mp4', 'webm', 'mov', 'avi'}
POSTS_PER_PAGE = 10  # Pagination
COMMENTS_PER_PAGE = 5  # Comments pagination

app.config['MAX_CONTENT_LENGTH'] = VERCEL_MAX_PAYLOAD

# Payload validation functions
def calculate_request_size():
    """Calculate the approximate size of the current request"""
    size = 0
    
    # Form data size
    if request.form:
        for key, value in request.form.items():
            size += len(str(key).encode('utf-8')) + len(str(value).encode('utf-8'))
    
    # File size
    if request.files:
        for key, file in request.files.items():
            if file and file.filename:
                # Seek to end to get size, then back to beginning
                file.seek(0, 2)
                file_size = file.tell()
                file.seek(0)
                size += file_size
    
    return size

def validate_payload_size():
    """Validate that the request doesn't exceed Vercel's 3MB limit"""
    size = calculate_request_size()
    if size > VERCEL_MAX_PAYLOAD:
        return False, f"Request too large ({size/1024/1024:.1f}MB). Maximum allowed: 3MB"
    return True, size

def validate_text_content(content, max_length, field_name):
    """Validate text content length"""
    if not content:
        return True, ""
    
    if len(content.encode('utf-8')) > max_length:
        return False, f"{field_name} too long. Maximum: {max_length} bytes"
    return True, ""

# Maintenance mode check
@app.before_request
def check_maintenance_mode():
    """Check if maintenance mode is enabled"""
    maintenance_mode = os.environ.get('MAINTENANCE_MODE', '').lower()
    if maintenance_mode in ['true', '1', 'yes', 'on']:
        # Allow access to static files for the maintenance page
        if request.endpoint and request.endpoint.startswith('static'):
            return None
        return render_template('maintenance.html'), 503

# Initialize in-memory storage
logging.info("Using in-memory storage with backup functionality")
if os.environ.get('BACKUP_URL'):
    logging.info(f"Backup URL configured: {os.environ.get('BACKUP_URL')}")
else:
    logging.warning("No BACKUP_URL configured - backups disabled")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Note: File path functions removed - now using Vercel blob storage directly


def load_posts():
    """Load all posts from memory storage"""
    try:
        posts = memory_storage.get_data('posts', [])
        # Sort by timestamp descending (newest first)
        return sorted(posts,
                      key=lambda x: x.get('timestamp', ''),
                      reverse=True)
    except Exception as e:
        logging.error(f"Error loading posts: {e}")
        return []


def load_comments():
    """Load all comments from Vercel blob storage"""
    try:
        data = memory_storage.get_data('comments', {})
        # Ensure data is a dictionary, not a list
        if isinstance(data, list):
            logging.warning("Comments data is a list, converting to empty dict")
            return {}
        return data
    except Exception as e:
        logging.error(f"Error loading comments: {e}")
        return {}


def load_likes():
    """Load all likes from Vercel blob storage"""
    try:
        data = memory_storage.get_data('likes', {})
        # Ensure data is a dictionary, not a list
        if isinstance(data, list):
            logging.warning("Likes data is a list, converting to empty dict")
            return {}
        return data
    except Exception as e:
        logging.error(f"Error loading likes: {e}")
        return {}


def load_hall_of_fame():
    """Load hall of fame posts from Vercel blob storage"""
    try:
        return memory_storage.get_data('hall_of_fame', [])
    except Exception as e:
        logging.error(f"Error loading hall of fame: {e}")
        return []


def load_hall_of_shame():
    """Load hall of shame posts from Vercel blob storage"""
    try:
        return memory_storage.get_data('hall_of_shame', [])
    except Exception as e:
        logging.error(f"Error loading hall of shame: {e}")
        return []


def load_videos():
    """Load all videos from Vercel blob storage"""
    try:
        videos = memory_storage.get_data('videos', [])
        # Sort by timestamp descending (newest first)
        return sorted(videos,
                      key=lambda x: x.get('timestamp', ''),
                      reverse=True)
    except Exception as e:
        logging.error(f"Error loading videos: {e}")
        return []


def save_videos(videos):
    """Save videos to Vercel blob storage"""
    try:
        return memory_storage.set_data('videos', videos)
    except Exception as e:
        logging.error(f"Error saving videos: {e}")
        return False


def create_video(username, title, description, filename):
    """Create a new video"""
    video = {
        'id': str(uuid.uuid4()),
        'username': username,
        'title': title,
        'description': description,
        'filename': filename,
        'timestamp': datetime.now().isoformat(),
        'views': 0
    }

    videos = load_videos()
    videos.append(video)

    if save_videos(videos):
        return video
    return None


def allowed_video_file(filename):
    """Check if file extension is allowed for videos"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in VIDEO_EXTENSIONS


def save_posts(posts):
    """Save posts to Vercel blob storage"""
    try:
        return memory_storage.set_data('posts', posts)
    except Exception as e:
        logging.error(f"Error saving posts: {e}")
        return False


def save_comments(comments):
    """Save comments to Vercel blob storage"""
    try:
        return memory_storage.set_data('comments', comments)
    except Exception as e:
        logging.error(f"Error saving comments: {e}")
        return False


def save_likes(likes):
    """Save likes to Vercel blob storage"""
    try:
        return memory_storage.set_data('likes', likes)
    except Exception as e:
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


def toggle_video_like(video_id, username):
    """Toggle like for a video by username"""
    return toggle_like(video_id, username)


def search_posts(query):
    """Search posts by content and username"""
    posts = load_posts()
    if not query:
        return posts

    query_lower = query.lower()
    filtered_posts = []

    for post in posts:
        if (query_lower in post.get('content', '').lower()
                or query_lower in post.get('username', '').lower()):
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
    flash(
        'Yo fam, that file is way too chonky! Keep it under 25MB for maximum Ohio rizz! 🚽',
        'error')
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
        post_comments_sorted = sorted(post_comments,
                                      key=lambda x: x.get('timestamp', ''),
                                      reverse=True)
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
        # First validate payload size for Vercel compatibility
        is_valid, size_info = validate_payload_size()
        if not is_valid:
            flash(f'{size_info} Please reduce file size or content length.', 'error')
            return render_template('create_post.html')
        
        username = request.form.get('username', '').strip()
        content = request.form.get('content', '').strip()

        # Validate inputs with proper limits
        if not username:
            flash('Bruh, you gotta drop your Skibidi username! No cap! 🚽', 'error')
            return render_template('create_post.html')

        # Validate username length
        is_valid, error_msg = validate_text_content(username, MAX_USERNAME_LENGTH, "Username")
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('create_post.html')

        if not content:
            flash('Yo, you forgot the Skibidi content! Drop some brainrot wisdom! 📸', 'error')
            return render_template('create_post.html')

        # Validate content length
        is_valid, error_msg = validate_text_content(content, TEXT_MAX_LENGTH, "Post content")
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('create_post.html')

        # Handle file upload to Vercel blob storage
        uploaded_filename = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename and file.filename != '':
                if file and file.filename and allowed_file(file.filename):
                    # Generate unique filename
                    secure_name = secure_filename(file.filename)
                    file_extension = secure_name.rsplit('.', 1)[1].lower()
                    unique_filename = f"{uuid.uuid4()}.{file_extension}"

                    try:
                        # Store file in memory
                        file_content = file.read()
                        file_size = len(file_content)
                        
                        # Check individual file size
                        if file_size > MAX_CONTENT_LENGTH:
                            flash(f'File too large! Maximum size: {MAX_CONTENT_LENGTH/1024/1024:.1f}MB', 'error')
                            return render_template('create_post.html')
                        
                        content_type = file.content_type or 'application/octet-stream'
                        
                        if memory_storage.store_file(file_content, unique_filename, content_type):
                            uploaded_filename = unique_filename
                            logging.info(f"File stored in memory: {unique_filename} ({file_size} bytes)")
                        else:
                            flash('Failed to upload your Skibidi content! Try again, sigma! 💀', 'error')
                            return render_template('create_post.html')
                    except Exception as e:
                        logging.error(f"Error uploading file: {e}")
                        flash(
                            'Failed to upload your Skibidi content! Try again, sigma! 💀',
                            'error')
                        return render_template('create_post.html')
                else:
                    flash(
                        'That file type is sus! Only upload valid Skibidi formats! 📁',
                        'error')
                    return render_template('create_post.html')

        # Create the post
        post = create_post(username, content, uploaded_filename)
        if post:
            flash(
                'Skibidi post created successfully! You\'re absolutely sigma! 🚽✨',
                'success')
            return redirect(url_for('index'))
        else:
            flash(
                'Failed to create your Skibidi post! The toilet gods are angry! 😱',
                'error')

    return render_template('create_post.html')


@app.route('/like/<post_id>', methods=['POST'])
def like_post(post_id):
    """Toggle like for a post"""
    username = request.form.get('username', '').strip()
    if not username:
        flash(
            'You need to provide a username to like posts! Drop your Skibidi name! 🚽',
            'error')
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
    # Validate payload size first
    is_valid, size_info = validate_payload_size()
    if not is_valid:
        flash(f'{size_info}', 'error')
        return redirect(url_for('index'))
    
    username = request.form.get('username', '').strip()
    comment_content = request.form.get('comment', '').strip()

    if not username:
        flash('Bruh, drop your username to comment! No anonymous Ohio energy! 🚽', 'error')
        return redirect(url_for('index'))

    # Validate username length
    is_valid, error_msg = validate_text_content(username, MAX_USERNAME_LENGTH, "Username")
    if not is_valid:
        flash(error_msg, 'error')
        return redirect(url_for('index'))

    if not comment_content:
        flash('You gotta write something sigma for your comment! 📸', 'error')
        return redirect(url_for('index'))

    # Validate comment length using our validation function
    is_valid, error_msg = validate_text_content(comment_content, MAX_COMMENT_LENGTH, "Comment")
    if not is_valid:
        flash(error_msg, 'error')
        return redirect(url_for('index'))

    comment = add_comment(post_id, username, comment_content)
    if comment:
        flash('Comment added! Your brainrot wisdom has been shared! ⚡',
              'success')
    else:
        flash('Failed to add comment! The Skibidi gods are upset! 😱', 'error')

    return redirect(url_for('index'))


@app.route('/hall-of-fame')
def hall_of_fame():
    """Hall of Fame page"""
    fame_posts = load_hall_of_fame()
    return render_template('hall_of_fame.html',
                           posts=fame_posts,
                           hall_type='fame')


@app.route('/hall-of-shame')
def hall_of_shame():
    """Hall of Shame page"""
    shame_posts = load_hall_of_shame()
    return render_template('hall_of_shame.html',
                           posts=shame_posts,
                           hall_type='shame')


@app.route('/comments/<post_id>')
def get_comments(post_id):
    """Get paginated comments for a post"""
    page = request.args.get('page', 1, type=int)
    comments = load_comments()
    post_comments = comments.get(post_id, [])

    # Sort comments by timestamp (newest first)
    post_comments_sorted = sorted(post_comments,
                                  key=lambda x: x.get('timestamp', ''),
                                  reverse=True)

    # Paginate comments
    pagination = paginate_comments(post_comments_sorted, page,
                                   COMMENTS_PER_PAGE)

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


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files from memory storage"""
    try:
        file_data = memory_storage.get_file(filename)
        if file_data:
            file_content = memory_storage.get_file_content(filename)
            if file_content:
                return Response(
                    file_content,
                    mimetype=file_data.get('content_type', 'application/octet-stream'),
                    headers={'Content-Disposition': f'inline; filename="{filename}"'}
                )
        
        logging.warning(f"File not found in memory: {filename}")
        return "File not found", 404
    except Exception as e:
        logging.error(f"Error serving file {filename}: {e}")
        return "Error serving file", 500


@app.route('/skibidi-scrolls')
def skibidi_scrolls():
    """Skibidi Scrolls video feed"""
    videos = load_videos()
    
    # Add likes data to videos
    likes = load_likes()
    for video in videos:
        video_id = video['id']
        video['like_count'] = len(likes.get(video_id, []))
    
    return render_template('skibidi_scrolls.html', videos=videos)


@app.route('/upload-scroll', methods=['GET', 'POST'])
def upload_scroll():
    """Upload new Skibidi Scroll video"""
    if request.method == 'POST':
        # Validate payload size first
        is_valid, size_info = validate_payload_size()
        if not is_valid:
            flash(f'{size_info} Please reduce video size or content length.', 'error')
            return render_template('upload_scroll.html')
        
        username = request.form.get('username', '').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        # Validate inputs with proper limits
        if not username:
            flash('Bruh, you gotta drop your Skibidi username! No cap! 🚽', 'error')
            return render_template('upload_scroll.html')

        # Validate username length
        is_valid, error_msg = validate_text_content(username, MAX_USERNAME_LENGTH, "Username")
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('upload_scroll.html')

        if not title:
            flash('Your Skibidi Scroll needs a sigma title! 📸', 'error')
            return render_template('upload_scroll.html')

        # Validate title length
        is_valid, error_msg = validate_text_content(title, TEXT_MAX_LENGTH, "Title")
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('upload_scroll.html')

        # Validate description length if provided
        if description:
            is_valid, error_msg = validate_text_content(description, TEXT_MAX_LENGTH, "Description")
            if not is_valid:
                flash(error_msg, 'error')
                return render_template('upload_scroll.html')

        # Handle video upload
        if 'video' not in request.files:
            flash('You need to upload a video for Skibidi Scrolls! 🎬', 'error')
            return render_template('upload_scroll.html')

        video_file = request.files['video']
        if not video_file.filename:
            flash('You need to upload a video for Skibidi Scrolls! 🎬', 'error')
            return render_template('upload_scroll.html')

        if video_file and video_file.filename and allowed_video_file(video_file.filename):
            # Generate unique filename
            secure_name = secure_filename(video_file.filename)
            file_extension = secure_name.rsplit('.', 1)[1].lower()
            unique_filename = f"scroll_{uuid.uuid4()}.{file_extension}"

            try:
                # Store video file in memory
                video_content = video_file.read()
                video_size = len(video_content)
                
                # Check individual video file size
                if video_size > MAX_CONTENT_LENGTH:
                    flash(f'Video too large! Maximum size: {MAX_CONTENT_LENGTH/1024/1024:.1f}MB', 'error')
                    return render_template('upload_scroll.html')
                
                content_type = video_file.content_type or f'video/{file_extension}'
                
                if memory_storage.store_file(video_content, unique_filename, content_type):
                    # Create the video
                    video = create_video(username, title, description, unique_filename)
                    if video:
                        flash('Skibidi Scroll uploaded successfully! Absolute sigma energy! 🚽✨', 'success')
                        logging.info(f"Video stored in memory: {unique_filename} ({video_size} bytes)")
                        return redirect(url_for('skibidi_scrolls'))
                    else:
                        flash('Failed to create your Skibidi Scroll! The toilet gods are angry! 😱', 'error')
                else:
                    flash('Failed to upload your Skibidi Scroll! Try again, sigma! 💀', 'error')
            except Exception as e:
                logging.error(f"Error uploading video: {e}")
                flash('Failed to upload your Skibidi Scroll! Try again, sigma! 💀', 'error')
        else:
            flash('That file type is sus! Only upload video formats for Skibidi Scrolls! 🎬', 'error')

    return render_template('upload_scroll.html')


@app.route('/like-video/<video_id>', methods=['POST'])
def like_video(video_id):
    """Toggle like for a video"""
    username = request.form.get('username', '').strip()
    if not username:
        return jsonify({'error': 'Username required'}), 400

    action, like_count = toggle_video_like(video_id, username)
    return jsonify({'action': action, 'like_count': like_count})


@app.route('/track-view/<video_id>', methods=['POST'])
def track_video_view(video_id):
    """Track a video view"""
    try:
        videos = load_videos()
        
        # Find and update the video
        for video in videos:
            if video['id'] == video_id:
                video['views'] = video.get('views', 0) + 1
                
                # Save updated videos
                if save_videos(videos):
                    return jsonify({'success': True, 'views': video['views']})
                else:
                    return jsonify({'success': False, 'error': 'Failed to save'}), 500
        
        return jsonify({'success': False, 'error': 'Video not found'}), 404
        
    except Exception as e:
        logging.error(f"Error tracking video view: {e}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@app.route('/api/posts')
def api_posts():
    """API endpoint for posts (if needed for AJAX)"""
    posts = load_posts()
    return jsonify(posts)

@app.route('/debug/storage')
def debug_storage():
    """Debug endpoint to check memory storage status"""
    all_data = memory_storage.get_all_data()
    
    debug_info = {
        'storage_keys': list(all_data.keys()),
        'posts_count': len(all_data.get('posts', [])),
        'files_count': len(all_data.get('files', {})),
        'files_stored': list(all_data.get('files', {}).keys())[:10],  # First 10 filenames
        'total_file_size': sum(f.get('size', 0) for f in all_data.get('files', {}).values()),
        'sample_post': all_data.get('posts', [])[0] if all_data.get('posts') else None,
        'memory_usage_estimate': len(str(all_data))
    }
    
    return jsonify(debug_info)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
