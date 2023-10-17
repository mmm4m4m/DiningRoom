from typing import Optional

from src.database.db import DBManager
from src.employees.models import EmployeeCreate, EmployeeRead


def get(*, db_manager: DBManager, employee_id: int) -> Optional[EmployeeRead]:
    params = (employee_id, )
    employee = db_manager.execute('SELECT id, user_id, position, first_name, last_name '
                                  'FROM employees '
                                  'WHERE id=? ',
                                  params=params)
    if not employee:
        return None 
    return EmployeeRead(id=employee[0], user_id=employee[1], position=employee[2], 
                        first_name=employee[3], last_name=employee[4])


def create(*, db_manager: DBManager, employee_in: EmployeeCreate) -> int:
    params = (employee_in.user_id, employee_in.position, 
              employee_in.first_name, employee_in.last_name)
    employee_id = db_manager.execute('INSERT INTO employees(user_id, position, first_name, last_name) '
                                     'VALUES(?, ?, ?, ?) ',
                                     params=params)
    return employee_id


def delete(*, db_manager: DBManager, employee_id: int) -> None:
    params = (employee_id, )
    db_manager.execute('DELETE FROM employees '
                       'WHERE id=? ',
                       params=params)
