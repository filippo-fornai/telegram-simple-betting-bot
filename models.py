from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger, index=True, primary_key=True)
    balance = Column(Integer, default=0)
    last_roll = Column(DateTime, default=None)

