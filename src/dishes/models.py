from typing import Optional

from pydantic import BaseModel, Field, field_validator


class DishBase(BaseModel):
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


class DishRead(DishBase):
    id: int
    products: list[str]


class DishList(BaseModel):
    dishes: Optional[list[DishRead]] = []


class DishUpdate(BaseModel):
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


class DishCreate(DishBase):
    product_ids: list[int]
