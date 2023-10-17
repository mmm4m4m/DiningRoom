from typing import Annotated
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from src.users.models import UserRead
from src.users.utils import get_current_user
from src.database.db import get_db_manager, DBManager
from src.orders.resolvers import create, get, get_all_waited_orders
from src.orders.utils import accept_order, complete_order
from src.orders.models import OrderCreate

router = APIRouter(prefix='/orders')


# @router.get('/my')
def get_current_user_orders(
        current_user: Annotated[UserRead, Depends(get_current_user)],
        db_manager: Annotated[DBManager, Depends(get_db_manager)]
    ):
    pass


@router.get('/{order_id}')
def get_order(db_manager: Annotated[DBManager, Depends(get_db_manager)], order_id: int):
    try:
        order = get(db_manager=db_manager, order_id=order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e
            )
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': f'Получен заказ №{order_id}', 'data': order}



@router.get('/all')
def all_waited_orders(db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        orders = get_all_waited_orders(db_manager=db_manager)
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 
            'detail': 'Получены все заказы со статусом "ожидание"', 
            'data': orders}


@router.post('/')
def create_order(
        db_manager: Annotated[DBManager, Depends(get_db_manager)], 
        order_in: OrderCreate
    ):
    try:
        order_id = create(db_manager=db_manager, order_in=order_in)
        db_manager.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_201_CREATED, 'detail': f'Создан заказ №{order_id}'}


@router.post('/{order_id}/accept')
def mark_order_as_accepted(
        employee_id: int, 
        order_id: int,
        db_manager: Annotated[DBManager, Depends(get_db_manager)]
    ):
    try:
        order = get(db_manager=db_manager, order_id=order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Заказа №{order_id} нет'
            )
        accept_order(db_manager=db_manager, order_id=order_id, employee_id=employee_id)
        db_manager.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': f'Заказ №{order_id} почемен как принятый'}


@router.post('/{order_id}/complete')
def mark_order_as_completed(
        order_id: int,
        db_manager: Annotated[DBManager, Depends(get_db_manager)]
    ):
    try:
        order = get(db_manager=db_manager, order_id=order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Заказа №{order_id} нет'
            )
        complete_order(db_manager=db_manager, order_id=order_id)
        db_manager.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': f'Заказ №{order_id} почемен как выполненный'}

