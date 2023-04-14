from pydantic import BaseModel
from typing import Text, List, Optional

class UserSchema(BaseModel):
    id: Optional[int]
    email: Optional[str]
    username: Optional[str]
    company_id: Optional[int]
    roles: Optional[str]
    status: Optional[str]
    permissions: Optional[List]

    class Config:
        orm_mode = True

class PermissionSchema(BaseModel):
    id: Optional[int]
    name: Optional[str] 
    description: Optional[str]
    mode: Optional[str] 
    model_name: Optional[str] 

    class Config:
        orm_mode = True
    
