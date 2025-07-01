import os
import json
import uuid
import logging
import math
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from storage_service import storage_service

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET",
                                "skibidi_sigma_ohio_rizz_2024")
app.config['UPLOAD_FOLDER'] = 'uploads'
# Configuration
DATA_FOLDER = 'data'

MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB
TEXT_MAX_LENGTH = 2048  # 2KB
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'mp3', 'wav',
    'doc', 'docx', 'zip'
}
VIDEO_EXTENSIONS = {'mp4', 'webm', 'mov', 'avi'}
POSTS_PER_PAGE = 10  # Pagination
COMMENTS_PER_PAGE = 5  # Comments pagination

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Migrate existing data on startup (if available)
try:
    if os.path.exists('data') or os.path.exists('uploads'):
        logging.info(
            "Found local data folders, attempting migration to Vercel blob storage..."
        )
        migration_success = storage_service.migrate_local_data()
        if migration_success:
            logging.info(
                "Successfully migrated local data to Vercel blob storage")
        else:
            logging.warning(
                "Migration completed with some errors - check logs for details"
            )
    else:
        logging.info(
            "No local data found, starting fresh with Vercel blob storage")
except Exception as e:
    logging.error(f"Error during migration: {e}")
    logging.info("Continuing with Vercel blob storage anyway")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Note: File path functions removed - now using Vercel blob storage directly


def load_posts():
    """Load all posts from Vercel blob storage"""
    try:
        posts = storage_service.get_json_data('posts', [])
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
        data = storage_service.get_json_data('comments', {})
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
        data = storage_service.get_json_data('likes', {})
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
        return storage_service.get_json_data('hall_of_fame', [])
    except Exception as e:
        logging.error(f"Error loading hall of fame: {e}")
        return []


def load_hall_of_shame():
    """Load hall of shame posts from Vercel blob storage"""
    try:
        return storage_service.get_json_data('hall_of_shame', [])
    except Exception as e:
        logging.error(f"Error loading hall of shame: {e}")
        return []


def load_videos():
    """Load all videos from Vercel blob storage"""
    try:
        videos = storage_service.get_json_data('videos', [])
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
        return storage_service.put_json_data('videos', videos)
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
        return storage_service.put_json_data('posts', posts)
    except Exception as e:
        logging.error(f"Error saving posts: {e}")
        return False


def save_comments(comments):
    """Save comments to Vercel blob storage"""
    try:
        return storage_service.put_json_data('comments', comments)
    except Exception as e:
        logging.error(f"Error saving comments: {e}")
        return False


def save_likes(likes):
    """Save likes to Vercel blob storage"""
    try:
        return storage_service.put_json_data('likes', likes)
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
        username = request.form.get('username', '').strip()
        content = request.form.get('content', '').strip()

        # Validate inputs
        if not username:
            flash('Bruh, you gotta drop your Skibidi username! No cap! 🚽',
                  'error')
            return render_template('create_post.html')

        if not content:
            flash(
                'Yo, you forgot the Skibidi content! Drop some brainrot wisdom! 📸',
                'error')
            return render_template('create_post.html')

        if len(content.encode('utf-8')) > TEXT_MAX_LENGTH:
            flash(
                f'That post is too long, fam! Keep it under {TEXT_MAX_LENGTH} bytes for maximum sigma energy! ⚡',
                'error')
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
                        # Read file content
                        file_content = file.read()
                        # Get content type
                        content_type = file.content_type or 'application/octet-stream'
                        
                        # Upload to Vercel blob storage
                        blob_url = storage_service.put_file(file_content, unique_filename, content_type)
                        if blob_url:
                            uploaded_filename = unique_filename
                            logging.info(f"File uploaded to blob storage: {blob_url}")
                        else:
                            flash(
                                'Failed to upload your Skibidi content! Try again, sigma! 💀',
                                'error')
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
    username = request.form.get('username', '').strip()
    comment_content = request.form.get('comment', '').strip()

    if not username:
        flash(
            'Bruh, drop your username to comment! No anonymous Ohio energy! 🚽',
            'error')
        return redirect(url_for('index'))

    if not comment_content:
        flash('You gotta write something sigma for your comment! 📸', 'error')
        return redirect(url_for('index'))

    if len(comment_content.encode('utf-8')) > 500:  # 500 bytes for comments
        flash(
            'That comment is too long! Keep it under 500 bytes for maximum brainrot! 💀',
            'error')
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
    """Serve uploaded files from Vercel blob storage"""
    try:
        # Get the blob URL for the file
        blob_url = storage_service.get_file_url(filename)
        if blob_url:
            # Redirect to the blob URL for direct serving
            return redirect(blob_url)
        else:
            logging.warning(f"File not found in blob storage: {filename}")
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
        username = request.form.get('username', '').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        # Validate inputs
        if not username:
            flash('Bruh, you gotta drop your Skibidi username! No cap! 🚽', 'error')
            return render_template('upload_scroll.html')

        if not title:
            flash('Your Skibidi Scroll needs a sigma title! 📸', 'error')
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
                # Read file content
                file_content = video_file.read()
                # Get content type
                content_type = video_file.content_type or f'video/{file_extension}'
                
                # Upload to Vercel blob storage
                blob_url = storage_service.put_file(file_content, unique_filename, content_type)
                if blob_url:
                    # Create the video
                    video = create_video(username, title, description, unique_filename)
                    if video:
                        flash('Skibidi Scroll uploaded successfully! Absolute sigma energy! 🚽✨', 'success')
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
