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
db_to_drop = os.getenv("DB_NAME")

# Connect to the default "postgres" database to issue DROP DATABASE
conn = psycopg2.connect(
    dbname="postgres",
    user=user,
    password=os.getenv("DB_PASSWORD"),  # no need to quote here since psycopg2 escapes it
    host=host,
    port=port
)

# Required for DROP DATABASE
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

def drop_database():
    try:
        cur.execute(f"DROP DATABASE {db_to_drop};")
        print(f"✅ Database '{db_to_drop}' has been dropped.")
    except psycopg2.errors.InvalidCatalogName:
        print(f"⚠️  Database '{db_to_drop}' does not exist.")
    except psycopg2.errors.ObjectInUse:
        print(f"⛔ Database '{db_to_drop}' is in use. Close all connections first.")
    finally:
        cur.close()
        conn.close()

# Call the function
drop_database()
