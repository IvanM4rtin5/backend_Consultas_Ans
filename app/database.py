from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os   
os.environ['PYTHONUTF8'] = '1'

db = SQLAlchemy()

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    connect_args={
        "client_encoding": "utf8"
    })

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = db.Model

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
