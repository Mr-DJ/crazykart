import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-replace-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///piltover.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = os.getenv('PORT', 18739)  # Default port for our LFSR server
    FLAG = os.getenv('FLAG', 'HEXTECH{default_flag_value}')  # Default flag for development
