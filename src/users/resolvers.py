from typing import Optional

from src.database.db import DBManager
from src.users.models import UserInput, UserRead
from src.users.utils import get_hashed_password


def get(*, db_manager: DBManager, user_id: int) -> Optional[UserRead]:
    params = (user_id, )
    user = db_manager.execute('SELECT id, email ' 
                              'FROM users WHERE id = ? ', 
                              params=params)
    if not user:
        return None
    return UserRead(id=user[0], email=user[1])    


def get_user_by_email(*, db_manager: DBManager, email: str) -> Optional[UserRead]:
    params = (email, )
    user = db_manager.execute('SELECT id, email ' 
                              'FROM users WHERE email=? ',
                              params=params)
    if not user:
        return None 
    return UserRead(id=user[0], email=user[1])


def get_user_hashed_password_by_email(*, db_manager: DBManager, email: str) -> Optional[str]:
    params = (email, )
    user = db_manager.execute('SELECT hashed_password ' 
                              'FROM users WHERE email=? ',
                              params=params)
    if not user:
        return None
    return user[0]


def create(*, db_manager: DBManager, user_in: UserInput) -> int:
    hashed_password = get_hashed_password(user_in.password.get_secret_value())
    params = (user_in.email, hashed_password)
    created_user_id = db_manager.execute('INSERT INTO users(email, hashed_password) '
                       'VALUES(?, ?) '
                       'RETURNING id ', 
                        params=params)[0]
    return created_user_id


def delete(*, db_manager: DBManager, user_email: str) -> None:
    params = (user_email, )
    db_manager.execute('DELETE FROM users ' 
                       'WHERE email = ? ', 
                       params=params)
