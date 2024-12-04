import os

class Config:
    # Base configuration
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///piltover.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask server settings
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    
    # Challenge-specific settings
    PORT = int(os.getenv('PORT', 18739))  # Cast to int for port number
    FLAG = os.getenv('FLAG', 'HEXTECH{default_flag_value}')
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes in seconds
