from typing import List
from Security.DTO.UserDto import UserDto
from pydantic import BaseModel



# Create a "database" to hold your data. This is just for example purposes. In
# a real world scenario you would likely connect to a SQL or NoSQL database.
class DataBase(BaseModel):
    user: List[UserDto]