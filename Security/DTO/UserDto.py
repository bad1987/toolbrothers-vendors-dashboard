from pydantic import BaseModel
# --------------------------------------------------------------------------
# Models and Data
# --------------------------------------------------------------------------
class UserDto(BaseModel):
    username: str
    email: str
    is_active: bool
    
class UserDtoCreate(BaseModel):
    username: str
    email: str
    password: str