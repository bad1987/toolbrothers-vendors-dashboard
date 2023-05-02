import json
from typing import Dict, List, Optional
from fastapi import Depends, HTTPException, Request, Response, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
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

route = APIRouter(prefix='', tags=['Handle account users'])
# templates = Jinja2Templates(directory="templates")
console = Console()

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @route.post("token")
# def login_for_access_token(
#     response: Response, 
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ) -> Dict[str, str]:
#     user = LoginController.authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
#     access_token = LoginController.create_access_token(data={"username": user.email})
    
#     # Set an HttpOnly cookie in the response. `httponly=True` prevents 
#     # JavaScript from reading the cookie.
#     response.set_cookie(
#         key=Settings.COOKIE_NAME, 
#         value=f"Bearer {access_token}", 
#         httponly=True
#     )  
#     return {Settings.COOKIE_NAME: access_token, "token_type": "bearer"}


@route.post("token")
def login_for_access_token(
    form_data: dict,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    user = LoginController.authenticate_user(form_data['username'], form_data['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = LoginController.create_access_token(data={"username": user.email})
    
    # Set an HttpOnly cookie in the response. `httponly=True` prevents 
    # JavaScript from reading the cookie. 
    p_user = UserSchema(**jsonable_encoder(user))
    return {Settings.COOKIE_NAME: access_token, "token_type": "bearer", "user": p_user}

# --------------------------------------------------------------------------
# Home Page
# --------------------------------------------------------------------------
# @route.get("/", response_class=HTMLResponse)
# def index(request: Request, db: Session = Depends(get_db)):
#     try:
#         user = LoginController.get_current_user_from_cookie(request, db)
#     except:
#         user = None
#     context = {
#         "user": user,
#         "request": request,
#     }
#     return templates.TemplateResponse("index.html", context)


# --------------------------------------------------------------------------
# Private Page
# --------------------------------------------------------------------------
# A private page that only logged in users can access.
# @route.get("/dashboard", response_class=HTMLResponse)
# def index(request: Request, db: Session = Depends(get_db)):
#     user = LoginController.get_current_user_from_cookie(request, db)
#     context = {
#         "user": user,
#         "request": request
#     }
#     return templates.TemplateResponse("private.html", context)

# --------------------------------------------------------------------------
# Register - GET
# --------------------------------------------------------------------------
# @route.get("/register", response_class=HTMLResponse)
# def register_get(request: Request):
#     context = {
#         "request": request
#     }
#     return templates.TemplateResponse("register.html", context)

# --------------------------------------------------------------------------
# Login - GET
# --------------------------------------------------------------------------
# @route.get("/auth/login", response_class=HTMLResponse)
# def login_get(request: Request, locale: str = 'de'):
#     translator.set_locale(locale)
#     context = {
#         "request": request
#     }
#     context.update(translator.get_data()[locale])

#     return templates.TemplateResponse("login.html", context)

# --------------------------------------------------------------------------
# Login - POST
# --------------------------------------------------------------------------

# @route.post("/auth/login", response_class=HTMLResponse)
# async def login_post(request: Request, locale: str = 'de', db: Session = Depends(get_db)):
#     translator.set_locale(locale)
#     form = LoginForm(request)
#     await form.load_data()
#     form.__dict__.update(translator.get_data()[locale])
#     print(form.__dict__)
#     if await form.is_valid():
#         try:
#             response = RedirectResponse("/", status.HTTP_302_FOUND)
#             res = login_for_access_token(response, form, db)
#             form.__dict__.update(msg="Login Successful!")
#             return response
#         except HTTPException:
#             form.__dict__.update(msg="")
#             error = translator.translate("login_wrong_cred")
#             form.__dict__.get("errors").append(error)
#             return templates.TemplateResponse("login.html", form.__dict__)
#     return templates.TemplateResponse("login.html", form.__dict__)

@route.post("/auth/login")
async def login_post(request: Request, db: Session = Depends(get_db)):
    credentials = json.loads(await request.body())
    response = JSONResponse(jsonable_encoder(credentials))
    res = login_for_access_token(credentials, db)
    res.update({'expired_at': Settings.ACCESS_TOKEN_EXPIRE_MINUTES})
    res.update({'cookie_name': Settings.COOKIE_NAME})
    return jsonable_encoder(res)

# --------------------------------------------------------------------------
# Register
# --------------------------------------------------------------------------

# @route.post("/register", response_class=HTMLResponse)
# async def register_post(request: Request, db: Session = Depends(get_db)):
#     form = RegisterForm(request)
#     await form.load_data()
#     if await form.is_valid():
#         try:
#             response = RedirectResponse("/auth/login", status.HTTP_302_FOUND)
#             is_save = LoginController.create_user_account(form, db)
#             if is_save == False:
#                 form.__dict__.update(msg="")
#                 form.__dict__.get("exist_user").append("This email exist")
#                 return templates.TemplateResponse("register.html", form.__dict__) 
#             return response
#         except HTTPException:
#             form.__dict__.update(msg="")
#             form.__dict__.get("errors").append("Incorrect Input")
#             return templates.TemplateResponse("register.html", form.__dict__)
#     return templates.TemplateResponse("register.html", form.__dict__)

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