from typing import Optional

from pydantic import BaseModel, field_validator


class OrderBase(BaseModel):
    client_id: int


class OrderCreate(OrderBase):
    dishes_ids: list[int]
    

class OrderAccept(BaseModel):
    employee_id: int


class OrderRead(OrderBase):
    id: int 
    status: str 
    dishes: list[str]
    employee_id: Optional[int] = None  
    

class OrderList(BaseModel):
    orders: Optional[list[OrderRead]]
