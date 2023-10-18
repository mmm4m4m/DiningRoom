from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float 
    quantity: int 


class ProductRead(ProductBase):
    id: int 


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass
