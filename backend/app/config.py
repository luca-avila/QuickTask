import os
import secrets

class Config:
    # Generate a secure random key if none is provided
    SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_hex(32)
    DATABASE_URL = 'sqlite:///backend/database.db'