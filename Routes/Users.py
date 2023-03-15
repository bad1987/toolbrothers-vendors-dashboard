from typing import Dict, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from Security.Controllers import LoginController
from Security.Settings import Settings
from Security.DTO.UserDto import UserDto



route = APIRouter(prefix='')
templates = Jinja2Templates(directory="templates")


@route.get("/users", response_class=HTMLResponse)
def index(request: Request, user: UserDto = Depends(LoginController.get_current_user_from_token)):
    context = {
        "user": user,
        "request": request
    }
    return templates.TemplateResponse("users.html", context)