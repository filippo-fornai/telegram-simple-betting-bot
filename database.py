import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from dotenv import load_dotenv
from models import Base
import urllib.parse

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{urllib.parse.quote_plus(os.getenv('DB_PASSWORD'))}@" \
               f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

print(f"Connecting to database at {DATABASE_URL}")
Engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=Engine)
ScopedSession = scoped_session(Session)


# # Run once to create tables
def init_db():
    Base.metadata.create_all(Engine)
