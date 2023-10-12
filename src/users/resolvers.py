from typing import Optional

from database.db import DBManager
from .models import UserInput, UserRead
from .utils import get_hashed_password


def get(*, db_manager: DBManager, user_id: int) -> Optional[UserRead]:
    params = (user_id, )
    user = db_manager.execute(query='SELECT id, email FROM users WHERE id = ?', params=params)
    if not user:
        return None
    return UserRead(id=user[0], email=user[1])    


def get_user_by_email(*, db_manager: DBManager, email: str) -> Optional[UserRead]:
    params = (email, )
    user = db_manager.execute(query='''
                            SELECT id, email FROM users WHERE email=?
                        ''', 
                        params=params)
    if not user:
        return None 
    return UserRead(id=user[0], email=user[1])


def get_user_hashed_password_by_email(*, db_manager: DBManager, email: str) -> Optional[str]:
    params = (email, )
    user = db_manager.execute(query='''
                            SELECT hashed_password FROM users WHERE email=?
                        ''',
                        params=params)
    if not user:
        return None
    return user[0]


def create(*, db_manager: DBManager, user_in: UserInput) -> None:
    hashed_password = get_hashed_password(user_in.password.get_secret_value())
    params = (user_in.email, hashed_password)
    db_manager.execute(query='''
                            INSERT INTO users(email, hashed_password) 
                            VALUES(?, ?)
                        ''', 
                        params=params)


def delete(*, db_manager: DBManager, user_id: int) -> None:
    params = (user_id, )
    db_manager.execute('''DELETE FROM users WHERE id = ?''', params=params)
