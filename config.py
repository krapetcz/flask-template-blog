# config.py
import os

# Get the absolute path of the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration class for the Flask application.
    Defines database location and security settings.
    """

    # Database URI - using SQLite database file in the project directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key used for session signing and security features
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zalozni-klic'

