from fastapi import Depends, APIRouter, Request
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

@route.post("/reset-password")
async def reset_password(token: str, new_password: str):
    # Check if the token is valid
    return True
