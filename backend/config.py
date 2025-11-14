# /backend/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis
    REDIS_URL = os.environ.get('REDIS_URL')
    
    # Upload Folder
    UPLOAD_FOLDER = os.path.join(basedir, 'tmp', 'uploads')