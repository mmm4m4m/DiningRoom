import sqlite3
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from src.database.db import DBManager, get_db_manager
from src.products.resolvers import get, update, create, delete
from src.products.models import ProductUpdate, ProductInput

router = APIRouter(prefix='/products')


@router.get('/{product_id}')
def get_product(product_id: int, db_manager: Annotated[DBManager, Depends(get_db_manager)]):
    try:
        product = get(db_manager=db_manager, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Продукт с id {product_id} не найден'
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': f'Получен продукт №{product_id}', 'data': product}


@router.post('/')
def create_product(
    product_in: ProductInput, 
    db_manager: Annotated[DBManager, Depends(get_db_manager)]
):
    try: 
        created_product_id = create(db_manager=db_manager, product_in=product_in)
        db_manager.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_201_CREATED, 'detail': f'Продукт №{created_product_id} создан'}


@router.delete('/{product_id}')
def delete_product(
    product_id: int,
    db_manager: Annotated[DBManager, Depends(get_db_manager)]
):
    try:
        delete(db_manager=db_manager, product_id=product_id)
        db_manager.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': 'Продукт удален'}


@router.put('/{product_id}')
def update_product(
        product_id: int, 
        product_in: ProductUpdate, 
        db_manager: Annotated[DBManager, Depends(get_db_manager)]
    ):
    try:
        product = get(db_manager=db_manager, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Продукт с id {product_id} не найден'
            )
        update(db_manager=db_manager, product_id=product_id, product_in=product_in)
        db_manager.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': 'Продукт обновлен'}
