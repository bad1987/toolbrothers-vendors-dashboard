from pydantic import BaseModel
from typing import Text, List, Optional

class UserSchema(BaseModel):
    id: Optional[int]
    email: Optional[str]
    username: Optional[str]
    company_id: Optional[int]
    roles: Optional[str]
    status: Optional[str]

class PermissionSchema:
    id = Optional[int]
    name = Optional[str] 
    description = Optional[str]