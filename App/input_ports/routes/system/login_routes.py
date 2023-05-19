import json, time, datetime
from typing import Dict, List
from fastapi import Depends, HTTPException, Request, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from rich.console import Console
from fastapi.encoders import jsonable_encoder
from App.core.auth.Configs.OAuth2PasswordBearerWithCookie import OAuth2PasswordBearerWithCookie
from App.core.auth.Configs.Settings import Settings
from App.core.use_cases.authentication_use_case import AuthenticationUsecase
from App.output_ports.db.Connexion import SessionLocal

import i18n
from App.Http.Schema.UserSchema import UserSchema

from App.core.auth import LoginController

# instantiate a new translator class
translator = i18n.Translator('languages/')

route = APIRouter(prefix='', tags=['Handle account users'], include_in_schema=False)
# templates = Jinja2Templates(directory="templates")
console = Console()

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@route.post("token")
def login_for_access_token(
    request: Request,
    form_data: dict,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    
    auth_usecase = AuthenticationUsecase(db)
    result = auth_usecase.login_access_token(request=request, form_data=form_data)

    return result

@route.post("/auth/login")
async def login_post(request: Request, db: Session = Depends(get_db)):
    credentials = json.loads(await request.body())
    res = login_for_access_token(request, credentials, db)
    res.update({'expired_at': Settings.ACCESS_TOKEN_EXPIRE_MINUTES})
    res.update({'cookie_name': Settings.COOKIE_NAME})
    return jsonable_encoder(res)

# --------------------------------------------------------------------------
# Logout
# --------------------------------------------------------------------------
@route.get("/auth/logout", response_class=HTMLResponse)
def login_get():
    response = RedirectResponse(url="/")
    response.delete_cookie(Settings.COOKIE_NAME)
    return response

@route.get('/auth/refresh')
async def refresh_token(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in"
        )
    access_token = LoginController.create_access_token(data={"username": user.email})
    context = {Settings.COOKIE_NAME: access_token, "token_type": "bearer"}
    context.update({'expired_at': Settings.ACCESS_TOKEN_EXPIRE_MINUTES})
    context.update({'cookie_name': Settings.COOKIE_NAME})
    return jsonable_encoder(context)


@route.post("/forgot-password")
async def forgot_password(request: Request, db_local: Session = Depends(get_db)):
    auth_usecase = AuthenticationUsecase(db_local)
    return auth_usecase.forgotten_password(request)

@route.post("/reset-password/{token}")
async def reset_password(token: str, request: Request, db_local: Session = Depends(get_db)):
    auth_usecase = AuthenticationUsecase(db_local)
    return auth_usecase.reset_password(request=request, token=token)
