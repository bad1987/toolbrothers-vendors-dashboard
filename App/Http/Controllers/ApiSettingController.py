from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from Security.Controllers import LoginController
from rich.console import Console
from Database.Models import User
from datetime import datetime, timedelta
import jwt

from Security.Settings import Settings
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

console = Console()

class ApiSettingController:
    def generate_token_for_api (request: Request, db_local: Session):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        userToken = db_local.query(User).filter(User.id == user.id).first()
        
        expire_time = datetime.utcnow() + timedelta(days=Settings.API_TOKEN_EXPIRE_DAYS)
        playload = {"exp": expire_time, "email": userToken.email}
        encoded_token = jwt.encode(playload, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        
        userToken.api_token = encoded_token
        db_local.commit()
        
        return encoded_token
 
    def get_token_api (request: Request, db_local: Session):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        userToken = db_local.query(User).filter(User.id == user.id).first()
        
        return userToken.api_token

    async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        # get token from credentials
        token = credentials.credentials
        # sanitize token
        token = token[7:]
        # validate token
        try:
            payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=Settings.ALGORITHM)
            return payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")