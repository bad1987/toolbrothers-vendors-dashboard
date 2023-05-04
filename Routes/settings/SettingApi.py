import time
from fastapi import Depends, HTTPException,Request, APIRouter, status
from App.Enums.UserRoleEnum import ModelNameEnum
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.ApiSettingController import ApiSettingController
from typing import List
from Decorators.auth_decorators import requires_permission
from Security.Acls.RoleChecker import Role_checker
from App.Http.Schema.UserSchema import ApiSetting
from fastapi.encoders import jsonable_encoder
from Routes.Users import is_authenticated

console = Console()

route = APIRouter(prefix='/setting', tags=['Get token api from user'], include_in_schema=False)

roles_checker = Role_checker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#Connexion from cscart database

def get_db_cscart():
    db_cscart = CscartSession()
    try:
        yield db_cscart
    finally:
        db_cscart.close()


def timestamp_to_date(s):
    return time.ctime(s)

@route.get('/api-token-user')
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def generate_token_for_api(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    token = ApiSettingController.generate_token_for_api(request, db_local)
    return token

@route.get('/get-token-api')
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_token_for_api(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    token = ApiSettingController.get_token_api(request, db_local)
    return token
   
