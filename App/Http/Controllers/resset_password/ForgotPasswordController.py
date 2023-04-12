import jwt
from sqlalchemy.orm import Session
from fastapi import Request, status, HTTPException
from Security.Controllers import LoginController
from Database.Models import User
from fastapi.responses import JSONResponse
from schemas.Settings.PlentyMarketSchema import PlentyMarketSchema
from Services import SendEmail
from datetime import datetime, timedelta
import Setting
from rich.console import Console
console = Console()


class ForgotPasswordController:
    def send_reset_password_email(email: str, db_local: Session):
        expire_time = datetime.utcnow() + timedelta(hours=24)
        payload = {"sub": "1234567890", "exp": expire_time}
        encoded_token = jwt.encode(payload, "secret", algorithm="HS256")
        link = f"{Setting.SERVER_HOST}/reset-password?token={encoded_token}"
        
        user = db_local.query(User).filter(User.email == email).first()
        sender_email = "bruno.mafo@utrains.org"
        password = "mathematique1234./@#"
        recipient_email = "antoine.didier@toolbrothers.com"
        subject = f"{user.username} - Password recovery for user {user.username}"
        body = f"Click this link to reset your password: {link}"
        
        email = SendEmail.send_email(sender_email, password, recipient_email, subject, body)
        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='No account corresponds to this email address')  