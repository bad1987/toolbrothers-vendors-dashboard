import re
import time
from fastapi import Depends, Request, APIRouter
from App.Enums.UserRoleEnum import ModelNameEnum
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from typing import List
from Decorators.auth_decorators import requires_permission
from Security.Acls.RoleChecker import Role_checker
from App.Http.Schema.UserSchema import UserCreateSubVendorSchema
from Routes.Users import is_authenticated
from App.Http.Controllers.UserController import UserController

console = Console()


roles_checker = Role_checker()

route = APIRouter(prefix='/sub-vendor', tags=['Handle sub vendor'], include_in_schema=False)


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

@route.get("/get")
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_sub_vendor_by_vendor(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    return UserController.get_sub_vendor_for_vendor(db_local, request)

@route.post("/create")
@requires_permission('write', ModelNameEnum.SETTING_MODEL.value)
async def create_dub_vendor_by_vendor(request: Request, schema: UserCreateSubVendorSchema, db_local: Session = Depends(get_db)):
    return UserController.create_sub_vendor_by_vendor(request, schema, db_local)
