from pydantic import BaseModel


class OrderDishesList(BaseModel):
    order_id: int
    dishes_ids: list[int] 
