import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "my_super_secret_key_123456789"
    JWT_SECRET_KEY = "jwt_secret_key_123456789_very_secure"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False