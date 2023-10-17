from src.database.db import DBManager


def accept_order(*, db_manager: DBManager, order_id: int, employee_id: int):
    params = (employee_id, "accepted", order_id)
    accepted_order_id = db_manager.execute('UPDATE orders '
                                           'SET employee_id=?, status=? '
                                           'WHERE id=? '
                                           'RETURNING id ',
                                           params=params)
    return accepted_order_id


def complete_order(*, db_manager: DBManager, order_id: int):
    params = ("complete", order_id)
    accepted_order_id = db_manager.execute('UPDATE orders '
                                           'SET status=? '
                                           'WHERE id=? '
                                           'RETURNING id ',
                                           params=params)
    return accepted_order_id
