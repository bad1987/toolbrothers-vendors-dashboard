import time
from fastapi import Depends, HTTPException,Request, APIRouter, status
from App.Enums.UserRoleEnum import ModelNameEnum
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.PlentyMarketController import PlentyMarketController
from typing import List
from Decorators.auth_decorators import requires_permission
from Security.Acls.RoleChecker import Role_checker
from schemas.Settings.PlentyMarketSchema import PlentyMarketSchema
from fastapi.encoders import jsonable_encoder
from Routes.Users import is_authenticated

console = Console()

route = APIRouter(prefix='/plenty-market')

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

@route.get('/vendor', response_model=List[PlentyMarketSchema], responses={200:{"model": PlentyMarketSchema}})
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_plenty_market_information(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    result = PlentyMarketController.get_plenty_market_information_by_vendor(request, db_local)
    res = []
    for u in result:
        res.append(PlentyMarketSchema(**jsonable_encoder(u)))
    return res

@route.post('/update')
@requires_permission('write', ModelNameEnum.SETTING_MODEL.value)
async def update_or_create(request: Request, schema: PlentyMarketSchema, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    return PlentyMarketController.update_or_add_setting_information(request, schema, db_local)
