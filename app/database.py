import psycopg2
from .config import DB_CONFIG

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def close_db_connection(connection): 
    if connection:
        connection.close()