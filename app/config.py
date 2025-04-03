import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"{os.getenv('DATABASE_URL')}?client_encoding=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
