from src.database.db import DBManager
from src.product_dishes.models import DishProductsRelation


def create(*, db_manager: DBManager, pd_in: DishProductsRelation) -> list[int]: 
    dish_id = pd_in.dish_id
    created_pd_list = []
    for product_id in pd_in.product_ids:
        params = (product_id, dish_id)
        pd_id = db_manager.execute('INSERT INTO product_dish(product_id, dish_id) '
                           'VALUES(?, ?) '
                           'RETURNING id ',
                           params=params)[0]
        created_pd_list.append(pd_id)
    return created_pd_list
