from typing import Dict, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from Security.Controllers import LoginController
from Security.Settings import Settings
from Security.DTO.UserDto import UserDto
from Database.Connexion import SessionLocal
from sqlalchemy.orm import Session
from Database.Models import User



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