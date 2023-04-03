from pydantic import BaseModel
from typing import Text, List, Optional

class ProductPriceSchema(BaseModel):
    price: Optional[float]
    
    class Config:
        orm_mode = True
