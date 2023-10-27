from pydantic import BaseModel


class ClientRead(BaseModel):
    id: int 
    user_id: int


class ClientCreate(BaseModel):
    user_id: int
