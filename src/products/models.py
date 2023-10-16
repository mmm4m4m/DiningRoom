from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class ProductRead(ProductBase):
    id: int 


class ProductInput(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass
