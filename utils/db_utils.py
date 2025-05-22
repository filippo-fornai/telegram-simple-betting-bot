from models import User
from sqlalchemy.orm.scoping import ScopedSession
from database import ScopedSession
from datetime import datetime

### UTILS
# BUILD_USER
def build_user(user_id:int, chat_id:int, balance:int, time:datetime):
    return User(
        user_id     = user_id,
        chat_id     = chat_id,
        balance     = balance,
        last_roll   = time
    )

### USER-RELATED FUNCTIONS
# GET_USER
def get_user(scoped_session,user_id:int, chat_id:int):
    user = scoped_session.query(User).filter_by(user_id=user_id, chat_id=chat_id).first()
    if user is None: return None
    return user

### CHAT-RELATED FUNCTIONS
# REMOVE_CHAT
def remove_chat(scoped_session,chat_id:int):
    users = scoped_session.query(User).filter_by(chat_id=chat_id).all()

    for user in users:
        scoped_session.delete(user)
