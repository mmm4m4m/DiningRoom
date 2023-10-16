from pydantic import BaseModel


class DishProductsRelation(BaseModel):
    dish_id: int 
    product_ids: list[int]
