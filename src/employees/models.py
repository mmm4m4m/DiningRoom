from pydantic import BaseModel


class EmployeeRead(BaseModel):
    id: int 
    user_id: int 
    position: str 
    first_name: str 
    last_name: str 


class EmployeeCreate(BaseModel):
    user_id: int 
    position: str 
    first_name: str 
    last_name: str 
