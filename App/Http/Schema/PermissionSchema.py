from pydantic import BaseModel
from typing import Text, List, Optional



class PermissionSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    mode: Optional[str]
    model_name: Optional[str]
    
    class Config:
        orm_mode = True