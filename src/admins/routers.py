from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.database.db import get_db_manager, DBManager
from src.users.resolvers import get as get_user
from src.employees.models import EmployeeCreate
from src.employees.resolvers import create as create_employee

router = APIRouter()


@router.post('/employee_create')
def create_employee(
        employee_in: EmployeeCreate, 
        db_manager: Annotated[DBManager, Depends(get_db_manager)]
    ):
    try:
        user_id = employee_in.user_id
        user = get_user(db_manager=db_manager, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Пользователь с id №{user_id} не найден'
            )
        created_employee_id = create_employee(db_manager=db_manager, employee_in=employee_in)
        db_manager.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )
    finally:
        db_manager.close()
    return {'status': status.HTTP_201_CREATED, 
            'detail': f'Создан новый сотрудник с id №{created_employee_id}'}
