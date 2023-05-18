from pydantic import BaseModel
from App.core.auth.Configs.Settings import Settings
from App.input_ports.schemas.UserSchema import UserSchema 


class LoginAccessTokenResponseSchema(BaseModel):
    Settings.COOKIE_NAME: str
    token_type: str
    user: UserSchema