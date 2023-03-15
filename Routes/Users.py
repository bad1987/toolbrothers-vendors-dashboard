from typing import Dict, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from Security.Controllers import LoginController
from Security.Settings import Settings
from Security.DTO.UserDto import UserDto, UserDtoCreate
from Database.Connexion import SessionLocal
from sqlalchemy.orm import Session
from Database.Models import User
from rich.console import Console
from fastapi.encoders import jsonable_encoder

console = Console()



route = APIRouter(prefix='')
templates = Jinja2Templates(directory="templates")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@route.get("/users", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)
    users = db.query(User).filter()
    context = {
        "user": user,
        "users": users,
        "request": request
    }
    return templates.TemplateResponse("users.html", context)

@route.get('/get-all-users', response_class=JSONResponse)
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db)
    console.log(user)
    users = db.query(User).all()

    return {'users': users}

@route.post('/users/', response_class=JSONResponse)
async def add_user(request: Request, db: Session = Depends(get_db)):
    try:
        datas = await request.json()
        current_user = LoginController.get_current_user_from_cookie(request, db)

        user = UserDtoCreate(**datas)

        ans = LoginController.create_user_account(user, db)


        if ans:
            return {
                'status': True,
                'message': 'OK',
                'current_user': current_user
            }

        return {
                'status': False,
                'message': 'An error occured, cannot create'
            }
    except:
        return {
                'status': False,
                'message': 'An error occured',
            }