from typing import Annotated

import sqlite3

from fastapi import APIRouter, HTTPException, status, Depends

from src.database.db import get_db_manager, DBManager
from src.users.utils import check_password
from src.users.models import UserInput, UserInput
from src.users.resolvers import (
    get_user_by_email, 
    create, 
    delete, 
    get_user_hashed_password_by_email
)

router = APIRouter()


@router.post('/register')
def create_user(user_in: UserInput, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        user = get_user_by_email(db_manager=db_manager, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Пользователь с таким email уже существует'
            )
        create(db_manager=db_manager, user_in=user_in)
        db_manager.commit()
        created_user = get_user_by_email(db_manager=db_manager, email=user_in.email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_201_CREATED, 'detail': 'Пользован создан', 'data': created_user}


@router.delete('/{user_email}')
def delete_user(user_email: str, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        user = get_user_by_email(db_manager=db_manager, email=user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Пользователя с почтой: {user_email} не существует'
            )
        delete(db_manager=db_manager, user_email=user_email)
        db_manager.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': 'Пользователь удален'}


@router.post('/login')
def login(user_in: UserInput, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        user = get_user_by_email(db_manager=db_manager, email=user_in.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Пользователя с таким email не сущесвует'
            )
        hashed_password = get_user_hashed_password_by_email(db_manager=db_manager, email=user_in.email)
        password_is_correct = check_password(password=user_in.password.get_secret_value(), hashed_password=hashed_password)
        if not password_is_correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверный пароль'
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': 'Авторизован', 'data': user}
