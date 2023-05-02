from pydantic import BaseModel, EmailStr
from typing import List, Optional
from App.Http.Schema.UserSchema import UserSchema
from App.Enums.UserEnums import UserStatusEnum
from App.Enums.UserRoleEnum import UserRoleEnum
# --------------------------------------------------------------------------
# Models and Data
# --------------------------------------------------------------------------


class Permission(BaseModel):
    value: Optional[int]
    text: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
class UserDto(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    status: UserStatusEnum
    company_id: int | None = None
    permissions: list | None = None
    roles: UserRoleEnum
    user_id: Optional[int]
    permissions: Optional[List[Permission]]

    class Config:
        orm_mode = True
    
class UserDtoCreate(BaseModel):
    username: str
    email: EmailStr
    status: UserStatusEnum
    permissions: list | None = None
    roles: UserRoleEnum


class UserListDto(BaseModel):
    users: List[UserSchema] = []
    permissions: List[Permission] = []