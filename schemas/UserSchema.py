from pydantic import BaseModel
from typing import Text, List, Optional
from App.Enums.UserEnums import UserStatusEnum
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Enums.LanguageEnum import LanguageEnum

class UserSchema(BaseModel):
    id: Optional[int]
    email: Optional[str]
    username: Optional[str]
    company_id: Optional[int]
    roles: Optional[UserRoleEnum]
    status: Optional[UserStatusEnum]
    permissions: Optional[List]
    firstname: Optional[str]
    lastname: Optional[str]
    default_language: Optional[LanguageEnum]

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
    
