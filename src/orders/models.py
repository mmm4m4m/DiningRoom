from typing import Optional

from pydantic import BaseModel, field_validator


class OrderBase(BaseModel):
    client_id: int 
    total_price: float

    @field_validator('total_price')
    @classmethod
    def validate_price(cls, value: float) -> float:
        if not value:
            return
        decimal_str = str(value)
        decimal_places = len(decimal_str.split('.')[1])
        if decimal_places != 2:
            value = round(value, 2)
        return value


class OrderCreate(OrderBase):
    pass 
    

class OrderAccept(BaseModel):
    employee_id: int


class OrderRead(OrderBase):
    id: int 
    status: str 
    employee_id: Optional[int] = None  
    

class OrderList(BaseModel):
    orders: Optional[list[OrderRead]]
