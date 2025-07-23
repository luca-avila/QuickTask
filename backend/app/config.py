import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_default_secret_key')
    DATABASE_URL = 'sqlite:///backend/database.db'