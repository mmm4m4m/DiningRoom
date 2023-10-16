from typing import Optional

from src.database.db import DBManager
from src.products.models import ProductInput, ProductRead, ProductUpdate


def get(*, db_manager: DBManager, product_id: int) -> Optional[ProductRead]:
    params = (product_id, )
    product = db_manager.execute('SELECT id, name ' 
                                 'FROM products ' 
                                 'WHERE id=? ',
                                 params=params)
    if not product:
        return None 
    return ProductRead(id=product[0], name=product[1])


def get_products_by_name(*, db_manager: DBManager, product_name: str) -> Optional[list[ProductRead]]:
    params = (product_name, )
    products = db_manager.execute('SELECT id, name '
                                  'FROM products '
                                  'WHERE name=? ',
                                  params=params,
                                  many=True)
    if not products:
        return None 
    product_list = [ProductRead(id=id, name=name) for id, name in products]
    return product_list


def create(*, db_manager: DBManager, product_in: ProductInput) -> int:
    params = (product_in.name, )
    created_product_id = db_manager.execute('INSERT INTO products(name) '
                       'VALUES(?) '
                       'RETURNING id ',
                       params=params)[0]
    return created_product_id


def update(*, db_manager: DBManager, product_id: int, product_in: ProductUpdate) -> None:
    params = (product_in.name, product_id)
    db_manager.execute('UPDATE products '
                       'SET name=? '
                       'WHERE id=? ',
                       params=params)


def delete(*, db_manager: DBManager, product_id: int) -> None:
    params = (product_id, )
    db_manager.execute('DELETE FROM products '
                       'WHERE id=? ',
                       params=params)
