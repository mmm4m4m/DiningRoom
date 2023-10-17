from src.database.db import DBManager


def user_is_employee(*, db_manager: DBManager, user_id: int) -> bool:
    params = (user_id, )
    is_employee = db_manager.execute('SELECT id '
                                     'FROM employees '
                                     'WHERE user_id=? ',
                                     params=params)
    return is_employee is not None
