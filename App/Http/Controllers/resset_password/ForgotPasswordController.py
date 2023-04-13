import jwt

import json
from sqlalchemy.orm import Session
from fastapi import Request, status, HTTPException
from Security.Controllers import LoginController
from Database.Models import User
from fastapi.responses import JSONResponse
from schemas.Settings.PlentyMarketSchema import PlentyMarketSchema
from Services import SendEmail
from datetime import datetime, timedelta
import Setting
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from rich.console import Console
console = Console()


class ForgotPasswordController:
    def send_reset_password_email(email: str, db_local: Session):
        user = db_local.query(User).filter(User.email == email).first()
        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='No account corresponds to this email address')  
        expire_time = datetime.utcnow() + timedelta(minutes=1)
        expired_ad = {"user_id": user.id, "exp": expire_time, "email": user.email}
        encoded_token = jwt.encode(expired_ad, "secret", algorithm="HS256")
        link = f"{Setting.SERVER_HOST}/reset-password?token={encoded_token}"
        
        console.log("tokennnnnnnnnnnnnnnn : ", jwt.decode(encoded_token, "secret", algorithms=['HS256'], verify=False)['exp'])
        
        sender_email = "no-reply@toolbrothers.com"
        password = "W6jS7S7xI2qbi8s"
        recipient_email = "mafobruno990@gmail.com"
        subject = f"{user.username} - Password recovery for user {user.username}"
        body = f"Click this link to reset your password: {link}"
        
        email = SendEmail.send_email(sender_email, password, recipient_email, subject, body)
        return JSONResponse(status_code=status.HTTP_200_OK, content='The email was sent successfully !!')
        
    
    def reset_password(token: str, password: str, db_local: Session):
        
        try:
            email = jwt.decode(token, "secret", algorithms=['HS256'], verify=False)['email']
            expired_ad = jwt.decode(token, "secret", algorithms=['HS256'], verify=False)['exp']

            if datetime.utcnow() < datetime.fromtimestamp(expired_ad):
                user = db_local.query(User).filter(User.email == email).first()
                if not user:
                    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='No account corresponds to this email address') 
            
                user.password = crypto.hash(f"{password}")
                
                db_local.commit()
                db_local.flush(user)
                
                return JSONResponse(status_code=status.HTTP_200_OK, content='Reset password successful !!') 
            else:
                return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content='Token is expired !!') 
        except:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Token is expired !!') 
        

