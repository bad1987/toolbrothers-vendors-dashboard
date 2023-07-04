from pydantic import BaseModel, EmailStr
from typing import Text, List, Optional
from App.Enums.UserEnums import UserStatusEnum
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Enums.LanguageEnum import LanguageEnum
from App.Http.Schema.PlatformSchema import PlatformSimpleSchema
from App.output_ports.models.Models import User

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
    connect_with_admin: Optional[bool]
    
    
    class Config:
        orm_mode = True

    @classmethod
    def from_user(cls, user: User) -> 'UserSchema':
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            company_id=user.company_id,
            roles=user.roles,
            status=user.status,
            permissions=[PermissionSchema(**{'id': perm.id, 'name': perm.name, 'description': perm.description}) for perm in user.permissions] if user.permissions else None,
            firstname=user.firstname,
            lastname=user.lastname,
            default_language=user.default_language,
            parent_id=user.parent_id,
            platform_id=user.platform_id,
            connect_with_admin= user.connect_with_admin,
            platform=None
        )

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