from typing import Optional

from src.database.db import DBManager
from src.products.models import ProductCreate, ProductRead, ProductUpdate


def product_read(product):
    return ProductRead(id=product[0], name=product[1], price=product[2], quantity=product[3])


def get(*, db_manager: DBManager, product_id: int) -> Optional[ProductRead]:
    params = (product_id, )
    product = db_manager.execute('SELECT id, name, price, quantity ' 
                                 'FROM products ' 
                                 'WHERE id=? ',
                                 params=params)
    if not product:
        return None 
    return product_read(product)


def get_products_by_name(*, db_manager: DBManager, product_name: str) -> Optional[list[ProductRead]]:
    params = (product_name, )
    products = db_manager.execute('SELECT id, name, price, quantity '
                                  'FROM products '
                                  'WHERE name=? ',
                                  params=params,
                                  many=True)
    if not products:
        return None 
    product_list = [product_read(product) for product in products]
    return product_list


def create(*, db_manager: DBManager, product_in: ProductCreate) -> int:
    params = (product_in.name, product_in.price, product_in.quantity)
    created_product_id = db_manager.execute('INSERT INTO products(name, price, quantity) '
                       'VALUES(?, ?, ?) '
                       'RETURNING id ',
                       params=params)[0]
    return created_product_id


def update(*, db_manager: DBManager, product_id: int, product_in: ProductUpdate) -> None:
    params = (product_in.name, product_in.price, product_in.quantity, product_id)
    db_manager.execute('UPDATE products '
                       'SET name=? '
                       'price=? '
                       'quantity=? '
                       'WHERE id=? ',
                       params=params)


def delete(*, db_manager: DBManager, product_id: int) -> None:
    params = (product_id, )
    db_manager.execute('DELETE FROM products '
                       'WHERE id=? ',
                       params=params)
