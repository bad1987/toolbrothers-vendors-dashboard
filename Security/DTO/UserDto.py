from pydantic import BaseModel, EmailStr
from typing import List, Optional
# --------------------------------------------------------------------------
# Models and Data
# --------------------------------------------------------------------------
class UserDto(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: str
    company_id: int | None = None
    permissions: list | None = None
    roles: str

    class Config:
        orm_mode = True
    
class UserDtoCreate(BaseModel):
    username: str
    email: EmailStr
    status: bool | str = False
    permissions: list | None = None
    roles: str

class Permission(BaseModel):
    value: int
    text: str

    class Config:
        orm_mode = True

class UserListDto(BaseModel):
    users: List[UserDto] = []
    permissions: List[Permission] = []