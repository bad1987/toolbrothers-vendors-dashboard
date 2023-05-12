from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import List, Optional

class ProductSchema(BaseModel):
    product_id: Optional[int]
    product_code: Optional[str]
    price: Optional[float]
    status: Optional[str]
    amount: Optional[int]
    product_type: Optional[str]
    weight: Optional[int]
    product: Optional[str]
    manual_change: Optional[bool]

class ProductListResponseSchema(BaseModel):
    products: List[ProductSchema]
    total: Optional[int]