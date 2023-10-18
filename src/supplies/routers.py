import sqlite3
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from src.database.db import DBManager, get_db_manager
from src.supplies.resolvers import create, get
from src.products.resolvers import create as create_product
from src.supply_product.resolvers import create as create_sp
from src.supply_product.models import SupplyProductsList, SupplyProductCreate


router = APIRouter(prefix='/supply')


@router.post('/')
def create_supply(
        sp_in: SupplyProductsList, 
        db_manager: Annotated[DBManager, Depends(get_db_manager)]
    ):
    try: 
        created_supply_id = create(db_manager=db_manager, supply_in=sp_in.supply)
        for product_in in sp_in.products:
            created_product_id = create_product(db_manager=db_manager, product_in=product_in)
            sp_create = SupplyProductCreate(supply_id=created_supply_id, product_id=created_product_id)
            create_sp(db_manager=db_manager, sp_in=sp_create)
        db_manager.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_201_CREATED, 'detail': 'Поставки и поставленные продукты созданы'}


@router.get('/{supply_id}')
def get_supply(
        supply_id: int, 
        db_manager: Annotated[DBManager, Depends(get_db_manager)]
    ):
    try: 
        supply = get(db_manager=db_manager, supply_id=supply_id)
        if not supply:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Не найдено поставки №{supply_id}'
            )
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_200_OK, 'detail': f'Поставка №{supply_id}', 'data': supply}

