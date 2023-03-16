from pydantic import BaseModel
# --------------------------------------------------------------------------
# Models and Data
# --------------------------------------------------------------------------
class UserDto(BaseModel):
    username: str
    email: str
    status: str
    company_id: int
    roles: str
    
class UserDtoCreate(BaseModel):
    username: str
    email: str
    password: str