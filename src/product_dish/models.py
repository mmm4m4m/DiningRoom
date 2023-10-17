from pydantic import BaseModel


class DishProductsList(BaseModel):
    dish_id: int 
    product_ids: list[int]
