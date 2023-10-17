from typing import Annotated
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from src.database.db import get_db_manager, DBManager
from src.users.resolvers import get as get_user, create as create_user
from src.users.models import UserCreate
from src.employees.models import EmployeeCreate
from src.employees.resolvers import create as create_employee

router = APIRouter()


@router.post('/employee_create')
def employee_create(
        user_in: UserCreate,
        employee_in: EmployeeCreate, 
        db_manager: Annotated[DBManager, Depends(get_db_manager)]
    ):
    try:
        created_user_id = create_user(db_manager=db_manager, user_in=user_in)
        created_employee_id = create_employee(db_manager=db_manager, 
                                              employee_in=employee_in, user_id=created_user_id)
        db_manager.commit()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_201_CREATED, 
            'detail': f'Создан новый сотрудник с id №{created_employee_id}'}
