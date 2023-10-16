from src.dishes.models import DishesRead, DishesList, DishesInput, DishesUpdate
from src.products.models import ProductRead
from src.database.db import DBManager


def get(*, db_manager: DBManager, dish_id: int) -> DishesRead:
    params = (dish_id, )
    dish = db_manager.execute('SELECT id, name, description, price '
                              'FROM dishes '
                              'WHERE id=? ',
                              params=params)
    if not dish:
        return None
    products = db_manager.execute('SELECT p.id, p.name '
                                  'FROM dishes d '
                                  'JOIN product_dish pd ON pd.dish_id=d.id '
                                  'JOIN products p ON p.id=pd.product_id '
                                  'WHERE d.id=? ',
                                  params=params,
                                  many=True)
    if products:
        products = [ProductRead(id=product[0], name=product[1]) for product in products]
    return DishesRead(id=dish[0], name=dish[1], description=dish[2], price=dish[3], products=products)


# def get_all(*, db_manager: DBManager) -> DishesList:
#     dishes_list = db_manager.execute('SELECT id, name, description, price '
#                                      'FROM dishes ')




def create(*, db_manager: DBManager, dish_in: DishesInput) -> int:
    params = (dish_in.name, dish_in.description, dish_in.price)
    created_dish_id = db_manager.execute('INSERT INTO dishes(name, description, price) '
                                         'VALUES(?, ?, ?) '
                                         'RETURNING id ',
                                         params=params)[0]
    return created_dish_id


def update(*, db_manager: DBManager, dish_id: int, dish_in: DishesUpdate):
    dish_in = dish_in.model_dump(exclude_none=True)
    if not dish_in:
        return 
    values_list = [] # создается список со строками вида key=value
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



def delete(*, db_manager: DBManager, dish_id: int):
    params = (dish_id, )
    db_manager.execute('DELETE FROM dishes '
                       'WHERE id=? ',
                       params=params)
    