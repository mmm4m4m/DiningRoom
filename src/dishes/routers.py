from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from src.database.db import get_db_manager, DBManager
from src.dishes.models import DishCreate
from src.product_dishes.resolvers import create as create_pd
from src.product_dishes.models import DishProductsRelation
from src.dishes.resolvers import create, get, get_all

router = APIRouter(prefix='/dishes')


@router.post('/')
def create_dish(dish_in: DishCreate, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        created_dish_id = create(db_manager=db_manager, dish_in=dish_in)
        pd_in = DishProductsRelation(dish_id=created_dish_id, product_ids=dish_in.product_ids)
        create_pd(db_manager=db_manager, pd_in=pd_in)
        db_manager.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_201_CREATED, 'detail': f'Блюдо №{created_dish_id} создано'}


@router.get('/')
def get_all_dishes(db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        dishes = get_all(db_manager=db_manager)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': 'Получены блюда', 'data': dishes}


@router.get('/{dish_id}')
def get_dish(dish_id: int, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        dish = get(db_manager=db_manager, dish_id=dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Блюдо с id №{dish_id} не найдено'
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': f'Получено блюдо №{dish_id}', 'data': dish}
