import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load credentials from .env
load_dotenv()

user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
new_db = os.getenv("DB_NAME")

# Connect to the default "postgres" database to issue CREATE DATABASE
conn = psycopg2.connect(
    dbname="postgres",
    user=user,
    password=os.getenv("DB_PASSWORD"),
    host=host,
    port=port
)

# Required for CREATE DATABASE
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()

def create_database():
    try:
        cur.execute(f"CREATE DATABASE {new_db};")
        print(f"✅ Database '{new_db}' created.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"⚠️ Database '{new_db}' already exists.")
    finally:
        cur.close()
        conn.close()
