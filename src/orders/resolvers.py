from typing import Optional

from src.database.db import DBManager
from src.orders.models import OrderCreate, OrderRead, OrderList


def order_read(order):
    return OrderRead(id=order[0], client_id=order[1], employee_id=order[2], 
                     total_price=order[3], status=order[4])


def get(*, db_manager: DBManager, order_id: int) -> Optional[OrderRead]:
    params = (order_id, )
    order = db_manager.execute('SELECT id, client_id, employee_id, total_price, status '
                               'FROM orders '
                               'WHERE id=? ',
                               params=params)
    if not order:
        return None 
    return order_read(order)


def get_all_waited_orders(*, db_manager: DBManager) -> Optional[OrderList]:
    params = ('waited', )
    order_list = db_manager.execute('SELECT id, client_id, employee_id, total_price, status '
                                    'FROM orders '
                                    'WHERE status=? ',
                                    params=params,
                                    many=True)
    if not order_list:
        return None 
    orders = [order_read(order) for order in order_list]
    return OrderList(orders=orders)



def create(*, db_manager: DBManager, order_in: OrderCreate) -> int:
    params = (order_in.client_id, order_in.total_price, 'waited')
    order_id = db_manager.execute('INSERT INTO orders(client_id, total_price, status) '
                                  'VALUES(?, ?, ?) '
                                  'RETURNING id ',
                                  params=params)[0]
    return order_id


def delete(*, db_manager: DBManager, order_id: int) -> None:
    params = (order_id, )
    db_manager.execute('DELETE FROM orders '
                       'WHERE id=? ',
                       params=params)
