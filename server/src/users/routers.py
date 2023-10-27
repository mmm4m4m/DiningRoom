from typing import Annotated
import sqlite3

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.database.db import get_db_manager, DBManager
from src.clients.resolvers import create as create_client
from src.clients.models import ClientCreate
from src.users.utils import check_password
from src.users.models import UserInput, UserInput, UserCreate
from src.users.resolvers import (
    get_user_by_email, 
    create, 
    delete, 
    get_user_hashed_password_by_email
)

router = APIRouter()


@router.post('/register')
def create_user(user_in: UserCreate, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        user = get_user_by_email(db_manager=db_manager, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Пользователь с таким email уже существует'
            )
        created_user_id = create(db_manager=db_manager, user_in=user_in)
        client_in = ClientCreate(user_id=created_user_id)
        create_client(db_manager=db_manager, client_in=client_in)
        db_manager.commit()
        created_user = get_user_by_email(db_manager=db_manager, email=user_in.email)
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': 'Пользован создан', 'data': created_user.model_dump()}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)


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
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': 'Пользователь удален'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)


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
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': 'Авторизован', 'data': user.model_dump()}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)
