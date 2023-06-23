from pydantic import BaseModel, EmailStr
from typing import Text, List, Optional
from App.Enums.UserEnums import UserStatusEnum
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Enums.LanguageEnum import LanguageEnum
from App.Http.Schema.PlatformSchema import PlatformSimpleSchema

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
    parent_id: Optional[int]
    platform_id: Optional[int]
    platform: Optional[PlatformSimpleSchema]

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

class PermissionReturnModel(BaseModel):
    text: Optional[str]
    description: Optional[str]
    value: Optional[int]
        
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
    permissions: List[PermissionReturnModel] = []
    platforms: List[PlatformSimpleSchema] = []