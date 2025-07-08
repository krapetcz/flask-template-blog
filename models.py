from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# SQLAlchemy database instance
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    Represents a user of the blog system.
    Includes login credentials and one-to-many relationship with articles.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One user can author many articles
    articles = db.relationship('Article', backref='author', lazy=True)


class Article(db.Model):
    """
    Represents a blog article.
    Each article belongs to one user and can contain multiple images.
    """

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key to the user who authored the article
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # One article can contain multiple images
    images = db.relationship('Image', backref='article', lazy=True)

class Image(db.Model):
    """
    Represents an image attached to a blog article.
    Stores filename and an optional caption.
    """
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))

    # Foreing key to the article this image belongs to
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)

