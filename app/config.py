import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    LOG_FILE = "app.log"