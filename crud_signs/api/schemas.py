from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

# CLIENT SCHEMAS
class ClientBase(BaseModel):
    name: str
    contact_info: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# ORDER SCHEMAS
class OrderBase(BaseModel):
    client_id: int
    description: str
    status: Optional[str] = "In Progress"
    due_date: datetime

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    description: Optional[str]
    status: Optional[str]
    due_date: Optional[datetime]

class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# AUTH SCHEMA
class Token(BaseModel):
    access_token: str
    token_type: str
