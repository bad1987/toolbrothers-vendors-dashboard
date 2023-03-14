from pydantic import BaseModel
# --------------------------------------------------------------------------
# Models and Data
# --------------------------------------------------------------------------
class UserDto(BaseModel):
    username: str
    name: str
    hashed_password: str
    
class UserDtoCreate(BaseModel):
    username: str
    email: str
    password: str
