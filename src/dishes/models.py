from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.products.models import ProductRead


class DishesBase(BaseModel):
    name: str = Field(max_length=255)
    description: str 
    price: float

    @field_validator('price')
    @classmethod
    def validate_price(cls, value: float) -> float:
        if not value:
            return
        decimal_str = str(value)
        decimal_places = len(decimal_str.split('.')[1])
        if decimal_places != 2:
            value = round(value, 2)
        return value


class DishesRead(DishesBase):
    id: int
    products: Optional[list[ProductRead]] = []


class DishesList(BaseModel):
    dishes: Optional[list[DishesRead]] = []


class DishesUpdate(BaseModel):
    name: Optional[str] = Field(max_length=255)
    description: Optional[str] = None
    price: Optional[float] = None

    @field_validator('price')
    @classmethod
    def validate_price(cls, value: float) -> float:
        if not value:
            return
        decimal_str = str(value)
        decimal_places = len(decimal_str.split('.')[1])
        if decimal_places != 2:
            value = round(value, 2)
        return value


class DishesInput(DishesBase):
    product_ids: list[int]
