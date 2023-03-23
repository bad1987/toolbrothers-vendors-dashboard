from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    company_id: int
    roles: str
    status: str
    