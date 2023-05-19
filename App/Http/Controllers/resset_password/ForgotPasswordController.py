import jwt

import json
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from App.core.Services.SendEmail import send_email
from App.output_ports.repositories.user_repository import UserRepository
import Setting
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from rich.console import Console
console = Console()


class ForgotPasswordController:
    def __init__(self, db_local) -> None:
        self.db_local = db_local
        self.user_reop = UserRepository(self.db_local)

    def send_reset_password_email(self, email: str):
        user = self.user_reop.get_user(email=email)
        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='No account corresponds to this email address')  
        expire_time = datetime.utcnow() + timedelta(minutes=1)
        expired_ad = {"user_id": user.id, "exp": expire_time, "email": user.email}
        encoded_token = jwt.encode(expired_ad, "secret", algorithm="HS256")
        link = f"{Setting.SERVER_HOST}/reset-password?token={encoded_token}"
        
        recipient_email = "b.mafo@toolbrothers.com"
        subject = f"{user.username} - Password recovery"
        body = f"Click this link to reset your password: {link}"
        
        email = send_email(recipient_email, subject, body)
        return JSONResponse(status_code=status.HTTP_200_OK, content='The email was sent successfully !!')
        
    
    def reset_password(self, token: str, password: str):
        
        try:
            email = jwt.decode(token, "secret", algorithms=['HS256'], verify=False)['email']
            expired_ad = jwt.decode(token, "secret", algorithms=['HS256'], verify=False)['exp']

            if datetime.utcnow() < datetime.fromtimestamp(expired_ad):
                user = self.user_reop.get_user(email=email)
                if not user:
                    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='No account corresponds to this email address') 
            
                password = crypto.hash(f"{password}")
                self.user_reop.update_password(new_hashed_password=password, email=user.email)
                
                return JSONResponse(status_code=status.HTTP_200_OK, content='Reset password successful !!') 
            else:
                return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='Token is expired !!') 
        except:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Token is expired !!') 
        

