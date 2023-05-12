from pydantic import BaseModel, EmailStr
from typing import Text, List, Optional
from App.Enums.UserEnums import UserStatusEnum
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Enums.LanguageEnum import LanguageEnum

class UserSchema(BaseModel):
    id: Optional[int]
    email: Optional[str]
    username: Optional[str]
    company_id: Optional[int]
    roles: Optional[UserRoleEnum] = None
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
        
class ApiSetting(BaseModel):
    api_token: Optional[str]
    

class UserCreateSubVendorSchema(BaseModel):
    email: Optional[str]
    username: Optional[str]
    status: Optional[UserStatusEnum]
    permissions: Optional[List]
    firstname: Optional[str]
    lastname: Optional[str]
    default_language: Optional[str]
    password: Optional[str]
    parent_id: Optional[int]
    
    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    status: UserStatusEnum
    permissions: list | None = None
    roles: UserRoleEnum


class UserListSchema(BaseModel):
    users: List[UserSchema] = []
    permissions: List[PermissionSchema] = []