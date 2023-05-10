from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import List

class OrdersSchema(BaseModel):
    order_id: int
    company_id: int
    status: str
    timestamp: datetime
    status: str
    firstname: str
    lastname: str
    email: str
    phone: str
    company: str
    total: float

    class Config:
        orm_mode = True

class OrderResponseModel(BaseModel):
    orders: List[OrdersSchema]
    total: int