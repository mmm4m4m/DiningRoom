from typing import Optional

from src.database.db import DBManager, get_db_manager
from src.orders.models import OrderCreate, OrderRead, OrderList


def order_read(order):
    dishes = order[4].split(', ')
    return OrderRead(id=order[0], client_id=order[1], employee_id=order[2], 
                     status=order[3], dishes=dishes)


def get(*, db_manager: DBManager, order_id: int) -> Optional[OrderRead]:
    params = (order_id, )
    order = db_manager.execute('SELECT o.id, o.client_id, o.employee_id, o.status, GROUP_CONCAT(d.name, ", ") '
                               'FROM orders o '
                               'JOIN order_dish od ON od.order_id=o.id '
                               'JOIN dishes d ON od.dish_id=d.id '
                               'WHERE o.id=? '
                               'GROUP BY o.id, o.client_id, o.employee_id, o.status ',
                               params=params)
    if not order:
        return None 
    return order_read(order)


def get_all_waited_orders(*, db_manager: DBManager) -> Optional[OrderList]:
    params = ('waited', )
    order_list = db_manager.execute('SELECT o.id, o.client_id, o.employee_id, o.status, GROUP_CONCAT(d.name, ", ") '
                                    'FROM orders o '
                                    'JOIN order_dish od ON od.order_id=o.id '
                                    'JOIN dishes d ON od.dish_id=d.id '
                                    'WHERE o.status=? '
                                    'GROUP BY o.id, o.client_id, o.employee_id, o.status ',
                                    params=params,
                                    many=True)
    if not order_list:
        return None 
    orders = [order_read(order) for order in order_list]
    return OrderList(orders=orders)


def create(*, db_manager: DBManager, order_in: OrderCreate) -> int:
    params = (order_in.client_id, 'waited')
    order_id = db_manager.execute('INSERT INTO orders(client_id, status) '
                                  'VALUES(?, ?) '
                                  'RETURNING id ',
                                  params=params)[0]
    return order_id


def delete(*, db_manager: DBManager, order_id: int) -> None:
    params = (order_id, )
    db_manager.execute('DELETE FROM orders '
                       'WHERE id=? ',
                       params=params)
