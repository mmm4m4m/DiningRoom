from src.database.db import DBManager
from src.order_dish.models import OrderDishesList


def create(*, db_manager: DBManager, od_in: OrderDishesList) -> list[int]: 
    order_id = od_in.order_id
    created_od_list = []
    for dish_id in od_in.dishes_ids:
        params = (order_id, dish_id)
        od_id = db_manager.execute('INSERT INTO order_dish(order_id, dish_id) '
                                   'VALUES(?, ?) '
                                   'RETURNING id ',
                                   params=params)[0]
        created_od_list.append(od_id)
    return created_od_list
