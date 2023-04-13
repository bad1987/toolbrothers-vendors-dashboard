from fastapi import Depends, APIRouter, Request, status
from fastapi.responses import JSONResponse
from Database.Connexion import SessionLocal
from sqlalchemy.orm import Session
from rich.console import Console
from fastapi.encoders import jsonable_encoder
from App.Http.Controllers.resset_password.ForgotPasswordController import ForgotPasswordController
import json
import i18n
from schemas.UserSchema import UserSchema

# instantiate a new translator class
translator = i18n.Translator('languages/')

route = APIRouter(prefix='')
console = Console()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@route.post("/forgot-password")
async def forgot_password(request: Request, db_local: Session = Depends(get_db)):
    credentials = json.loads(await request.body())
    response = JSONResponse(jsonable_encoder(credentials))
    result = ForgotPasswordController.send_reset_password_email(credentials['email'], db_local)
    return result

@route.post("/reset-password/{token}")
async def reset_password(token: str, request: Request, db_local: Session = Depends(get_db)):
    credentials = json.loads(await request.body())
    response = JSONResponse(jsonable_encoder(credentials))
    
    if credentials['password'] != credentials['confirm_password']:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Password and confirm password is not correct!') 
    
    result = ForgotPasswordController.reset_password(token, credentials['password'], db_local)
    # Check if the token is valid
    return result
