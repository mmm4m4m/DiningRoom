from src.database.db import DBManager
from src.supply_product.models import SupplyProductCreate


def create(*, db_manager: DBManager, sp_in: SupplyProductCreate) -> int:
    params = (sp_in.supply_id, sp_in.product_id)
    created_supply_product_id = db_manager.execute('INSERT INTO supply_product(supply_id, product_id) '
                                                   'VALUES(?, ?) ',
                                                   params=params)
    return created_supply_product_id
