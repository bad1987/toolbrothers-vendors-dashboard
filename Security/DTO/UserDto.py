from pydantic import BaseModel, EmailStr
from typing import List, Optional
from schemas.UserSchema import UserSchema
# --------------------------------------------------------------------------
# Models and Data
# --------------------------------------------------------------------------


class Permission(BaseModel):
    value: Optional[int]
    text: Optional[str]

    class Config:
        orm_mode = True
class UserDto(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: str
    company_id: int | None = None
    permissions: list | None = None
    roles: str
    permissions: Optional[List[Permission]]

    class Config:
        orm_mode = True
    
class UserDtoCreate(BaseModel):
    username: str
    email: EmailStr
    status: bool | str = False
    permissions: list | None = None
    roles: str


class UserListDto(BaseModel):
    users: List[UserSchema] = []
    permissions: List[Permission] = []