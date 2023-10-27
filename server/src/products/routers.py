import sqlite3
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.database.db import DBManager, get_db_manager
from src.products.resolvers import get, update, create, delete
from src.products.models import ProductUpdate, ProductCreate

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
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': f'Получен продукт №{product_id}', 'data': product.model_dump()}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)


@router.post('/')
def create_product(
    product_in: ProductCreate, 
    db_manager: Annotated[DBManager, Depends(get_db_manager)]
):
    try: 
        created_product_id = create(db_manager=db_manager, product_in=product_in)
        db_manager.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': f'Продукт №{created_product_id} создан'}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_data)


@router.delete('/{product_id}')
def delete_product(
    product_id: int,
    db_manager: Annotated[DBManager, Depends(get_db_manager)]
):
    try:
        product = get(db_manager=db_manager, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Продукт с id {product_id} не найден'
            )
        delete(db_manager=db_manager, product_id=product_id)
        db_manager.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': 'Продукт удален'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)


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
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    json_data = {'detail': 'Продукт обновлен'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_data)
