from pydantic import BaseModel
# --------------------------------------------------------------------------
# Models and Data
# --------------------------------------------------------------------------
class UserDto(BaseModel):
    id: int
    username: str
    email: str
    status: str
    company_id: int
    roles: str
    
class UserDtoCreate(BaseModel):
    username: str
    email: str
    password: str

class AdminDtoCreate(BaseModel):
    username: str
    email: str
    password: str | None = None
    permissions: list | None = None