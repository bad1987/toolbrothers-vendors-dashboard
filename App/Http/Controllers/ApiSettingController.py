from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from rich.console import Console
from datetime import datetime, timedelta
import jwt

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from App.core.auth import LoginController

from App.core.auth.Configs.Settings import Settings
from App.output_ports.repositories.user_repository import UserRepository

security = HTTPBearer()

console = Console()

class ApiSettingController:

    def __init__(self, db_local) -> None:
        self.db_local = db_local

    def generate_token_for_api (self, request: Request):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        user_repo = UserRepository(self.db_local)
        if user is None:
            return None
        encoded_token = user_repo.generate_api_token(email=user.email)
        return encoded_token
 
    def get_token_api (self, request: Request):
        user_repo = UserRepository(self.db_local)
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        if user is None:
            return None
        userToken = user_repo.get_user(email=user.email)
        
        return userToken.api_token

    async def validate_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        # get token from credentials
        token = credentials.credentials
        # sanitize token
        token = token.removeprefix("Bearer").strip()
        # validate token
        try:
            payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=Settings.ALGORITHM)
            return payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")