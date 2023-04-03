from pydantic import BaseModel
from typing import Text, List, Optional

class ProductDescriptionSchema(BaseModel):
    full_description: Optional[str]
    short_description: Optional[str]
    
    class Config:
        orm_mode = True

    
    