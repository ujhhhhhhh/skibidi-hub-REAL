from datetime import datetime


def init_models(db):
    """Initialize models with the database instance"""
    
    class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_hall_of_fame = db.Column(db.Boolean, default=False)
    is_hall_of_shame = db.Column(db.Boolean, default=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'content': self.content,
            'filename': self.filename,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'is_hall_of_fame': self.is_hall_of_fame,
            'is_hall_of_shame': self.is_hall_of_shame,
            'comments_count': len(self.comments),
            'likes_count': len(self.likes)
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'username': self.username,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Ensure one like per user per post
    __table_args__ = (db.UniqueConstraint('post_id', 'username', name='unique_user_post_like'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'username': self.username,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }