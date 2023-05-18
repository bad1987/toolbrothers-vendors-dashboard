
import json
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from App.Enums.UserEnums import UserStatusEnum
from App.Http.Controllers.resset_password.ForgotPasswordController import ForgotPasswordController
from App.core.auth import LoginController
from App.core.auth.Configs.Settings import Settings

from App.input_ports.schemas.AuthenticationSchema import LoginAccessTokenResponseSchema
from App.input_ports.schemas.UserSchema import UserSchema
from App.output_ports.repositories.authentication_repository import AuthenticationRepository


class AuthenticationUsecase:
    def __init__(self, db_local: Session) -> None:
        self.db = db_local
        self.auth_repo = AuthenticationRepository(self.db)
    
    def login_access_token(self,request: Request, form_data: dict) -> LoginAccessTokenResponseSchema:
        user = LoginController.authenticate_user(form_data['username'], form_data['password'], self.db)

        connected_ip = request.client.host
        attempt = self.auth_repo.get_attempts(connected_ip)
        if not user:
            if attempt is None:
                self.auth_repo.create_attempt(connected_ip)
            else:
                self.auth_repo.increment_attempt(connected_ip)
                
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        if user.status != UserStatusEnum.ACTIVE:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account is not active, please contact admins")
            
        access_token = LoginController.create_access_token(data={"username": user.email})

        if attempt != None:
            self.auth_repo.reset_attempt(connected_ip)
        p_user = UserSchema(**user.__dict__)
        
        return {Settings.COOKIE_NAME: access_token, "token_type": "bearer", "user": p_user}
    
    
    async def forgotten_password(self, request: Request):
        credentials = json.loads(await request.body())
        result = ForgotPasswordController.send_reset_password_email(credentials['email'], self.db)
        
        return result
    
    async def reset_password(self, request: Request, token: str):
        credentials = json.loads(await request.body())
        
        if credentials['password'] != credentials['confirm_password']:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content='Password and confirm password is not correct!') 
        
        result = ForgotPasswordController.reset_password(token, credentials['password'], self.db)
        # Check if the token is valid
        return result