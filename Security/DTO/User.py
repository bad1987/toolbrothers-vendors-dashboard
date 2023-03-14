from pydantic import BaseModel
# --------------------------------------------------------------------------
# Models and Data
# --------------------------------------------------------------------------
class User(BaseModel):
    username: str
    name: str
    hashed_password: str
