import json, time, datetime
from typing import Dict, List, Optional
from fastapi import Depends, HTTPException, Request, Response, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from App.Enums.UserEnums import UserStatusEnum
from Database.Models import Login_Attempt
from Security.OAuth2PasswordBearerWithCookie import OAuth2PasswordBearerWithCookie
from fastapi.security import OAuth2PasswordRequestForm
# from fastapi.templating import Jinja2Templates
from Security.Controllers import LoginController
from Security.Settings import Settings
from Security.DTO.UserDto import UserDto
from Security.Validator.LoginForm import LoginForm
from Security.Validator.RegisterForm import RegisterForm
from Database.Connexion import SessionLocal
from sqlalchemy.orm import Session
from rich.console import Console
from fastapi.encoders import jsonable_encoder

import i18n
from App.Http.Schema.UserSchema import UserSchema

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
    user = LoginController.authenticate_user(form_data['username'], form_data['password'], db)
    # search if previous attempts
    now = datetime.datetime.now()
    future = now + datetime.timedelta(minutes=1)

    timestamp = time.mktime(future.timetuple())

    connected_ip = request.client.host
    attempt = db.query(Login_Attempt).filter(Login_Attempt.ip == connected_ip).first()
    if not user:
        if attempt is None:
            attempt = Login_Attempt()

            attempt.ip = connected_ip
            attempt.count = 1
            db.add(attempt)
        else:
            attempt.count += 1
            if attempt.count >= 3:
                attempt.timestamp = timestamp

        db.commit()

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    if user.status != UserStatusEnum.ACTIVE:
        console.log(user.status.value)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account is not active, please contact admins")
    access_token = LoginController.create_access_token(data={"username": user.email})

    if attempt != None:
        attempt.count = 0
        db.commit()
    
    # Set an HttpOnly cookie in the response. `httponly=True` prevents 
    # JavaScript from reading the cookie. 
    # p_user = UserSchema(**jsonable_encoder(user))
    dictio = UserSchema(id=user.id, username=user.username, company_id=user.company_id, email=user.email, default_language=user.default_language, firstname=user.firstname, lastname=user.lastname, roles=user.roles, status=user.status, permissions=user.permissions)
    # console.log(user.__dict__)
    # console.log()
    p_user = UserSchema(**user.__dict__)
    console.log(p_user)
    return {Settings.COOKIE_NAME: access_token, "token_type": "bearer", "user": p_user}


@route.post("/auth/login")
async def login_post(request: Request, db: Session = Depends(get_db)):
    credentials = json.loads(await request.body())
    response = JSONResponse(jsonable_encoder(credentials))
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