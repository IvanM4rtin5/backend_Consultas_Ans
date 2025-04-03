from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os   
os.environ['PYTHONUTF8'] = '1'

db = SQLAlchemy()

# Criar a engine do SQLAlchemy
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Criar a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    connect_args={
        "client_encoding": "utf8"
    })

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
