from pydantic import BaseModel

from src.products.models import ProductCreate
from src.supplies.models import SupplyCreate


class SupplyProductsList(BaseModel):
    supply: SupplyCreate
    products: list[ProductCreate]


class SupplyProductCreate(BaseModel):
    supply_id: int 
    product_id: int
