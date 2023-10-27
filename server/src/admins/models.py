from pydantic import BaseModel, Field


class AdminRead(BaseModel):
    id: int
    user_id: int
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)


class AdminCreate(BaseModel):
    user_id: int 
    first_name: str 
    last_name: str 
