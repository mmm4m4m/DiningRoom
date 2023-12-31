from typing import Annotated

import sqlite3

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from src.database.db import get_db_manager, DBManager
from src.dishes.models import DishCreate
from src.product_dish.resolvers import create as create_pd
from src.product_dish.models import DishProductsList
from src.dishes.resolvers import create, get, get_all, delete

router = APIRouter(prefix='/dishes')


@router.post('/')
def create_dish(dish_in: DishCreate, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        created_dish_id = create(db_manager=db_manager, dish_in=dish_in)
        pd_in = DishProductsList(dish_id=created_dish_id, product_ids=dish_in.product_ids)
        create_pd(db_manager=db_manager, pd_in=pd_in)
        db_manager.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': f'Блюдо №{created_dish_id} создано'}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_data)

@router.get('/')
def get_all_dishes(db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        dishes = get_all(db_manager=db_manager)
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': 'Получены блюда', 'data': dishes.model_dump()}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)

@router.get('/{dish_id}')
def get_dish(dish_id: int, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        dish = get(db_manager=db_manager, dish_id=dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Блюдо с id №{dish_id} не найдено'
            )
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': f'Получено блюдо №{dish_id}', 'data': dish.model_dump()}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)

@router.delete('/{dish_id}')
def delete_dish(dish_id: int, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        dish = get(db_manager=db_manager, dish_id=dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Блюдо с id №{dish_id} не найдено'
            )
        delete(db_manager=db_manager, dish_id=dish_id)
        db_manager.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': f'Блюдо №{dish_id} удалено'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)
