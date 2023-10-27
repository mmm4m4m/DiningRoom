from pydantic import BaseModel

from src.products.models import ProductRead


class SupplyRead(BaseModel):
    id: int 
    admin_id: int
    products: list[ProductRead]


class SupplyCreate(BaseModel):
    admin_id: int
    