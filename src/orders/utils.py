from src.database.db import DBManager, get_db_manager


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


def get_order_total_price(*, db_manager: DBManager, order_id: int):
    params = (order_id, )
    total_price = db_manager.execute('SELECT SUM(d.price) '
                                     'FROM dishes d '
                                     'JOIN order_dish od ON od.dish_id=d.id '
                                     'WHERE od.order_id=? ',
                                     params=params)[0]
    return total_price
