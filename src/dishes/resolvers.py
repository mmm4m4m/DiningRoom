from typing import Optional

from src.dishes.models import DishRead, DishList, DishCreate, DishUpdate
from src.database.db import DBManager, get_db_manager


def get(*, db_manager: DBManager, dish_id: int) -> Optional[DishRead]:
    params = (dish_id, )
    dish = db_manager.execute('SELECT d.id, d.name, d.description, d.price, GROUP_CONCAT(p.name, ", ") '
                              'FROM dishes d '
                              'JOIN product_dish pd ON pd.dish_id=d.id '
                              'JOIN products p ON pd.product_id=p.id '
                              'WHERE d.id=? '
                              'GROUP BY d.id, d.name, d.description, d.price ',
                              params=params)
    if not dish:
        return None
    products = dish[4].split(', ')
    return DishRead(id=dish[0], name=dish[1], description=dish[2], price=dish[3], products=products)


def get_all(*, db_manager: DBManager) -> Optional[DishList]:
    dish_list = db_manager.execute('SELECT d.id, d.name, d.description, d.price, GROUP_CONCAT(p.name, ", ") '
                                   'FROM dishes d '
                                   'JOIN product_dish pd ON pd.dish_id=d.id '
                                   'JOIN products p ON pd.product_id=p.id '
                                   'GROUP BY d.id, d.name, d.description, d.price ',
                                   many=True)
    if not dish_list:
        return None
    dishes = []
    for dish in dish_list:
        products = dish[4].split(', ')
        dish_read = DishRead(id=dish[0], name=dish[1], description=dish[2], price=dish[3], products=products)
        dishes.append(dish_read)
    return DishList(dishes=dishes)


def create(*, db_manager: DBManager, dish_in: DishCreate) -> int:
    params = (dish_in.name, dish_in.description, dish_in.price)
    created_dish_id = db_manager.execute('INSERT INTO dishes(name, description, price) '
                                         'VALUES(?, ?, ?) '
                                         'RETURNING id ',
                                         params=params)[0]
    return created_dish_id


def update(*, db_manager: DBManager, dish_id: int, dish_in: DishUpdate) -> None:
    dish_in = dish_in.model_dump(exclude_none=True)
    if not dish_in:
        return None
    values_list = [] # заполняется строками вида key=value
    for key, value in dish_in.items():
        if type(value) == str: 
            val = f'{key}="{value}"' # ex: name="test"
        else:
            val = f'{key}={value}' # ex: price=13.45
        values_list.append(val)
    values_str = ', '.join(values_list)
    query = 'UPDATE dishes ' + 'SET ' + values_str + 'WHERE dish_id=? '
    params = (dish_id, )
    db_manager.execute(query,
                       params=params)



def delete(*, db_manager: DBManager, dish_id: int) -> None:
    params = (dish_id, )
    db_manager.execute('DELETE FROM dishes '
                       'WHERE id=? ',
                       params=params)
    