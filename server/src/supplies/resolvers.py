from typing import Optional

from src.database.db import DBManager
from src.supplies.models import SupplyCreate, SupplyRead
from src.products.resolvers import product_read


def get(*, db_manager: DBManager, supply_id: int) -> Optional[SupplyRead]:
    params = (supply_id, )
    supply = db_manager.execute('SELECT id, admin_id '
                                'FROM supplies '
                                'WHERE id=? ',
                                params=params)
    if not supply:
        return None 
    product_list = db_manager.execute('SELECT products.id, name, price, quantity '
                                      'FROM products '
                                      'JOIN supply_product ON products.id=supply_product.product_id '
                                      'WHERE supply_product.supply_id=? ',
                                      params=params,
                                      many=True)
    products = [product_read(product) for product in product_list]
    return SupplyRead(id=supply[0], admin_id=supply[1], products=products)


def create(*, db_manager: DBManager, supply_in: SupplyCreate) -> int:
    params = (supply_in.admin_id, )
    created_supply_id = db_manager.execute('INSERT INTO supplies(admin_id) '
                                           'VALUES(?) '
                                           'RETURNING id ',
                                           params=params)[0]
    return created_supply_id
