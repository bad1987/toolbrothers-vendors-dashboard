import re
import time
from fastapi import Depends, Request, APIRouter
from App.Enums.UserRoleEnum import ModelNameEnum
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from typing import Dict, List
from Database.Models import Permission, User
from Decorators.auth_decorators import requires_permission
from Security.Acls.RoleChecker import Role_checker
from App.Http.Schema.UserSchema import UserCreateSubVendorSchema, UserSchema
from Routes.Users import is_authenticated
from App.Http.Controllers.UserController import UserController
from Security.DTO.UserDto import UserListDto

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

@route.get("/get", response_model=UserListDto)
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_sub_vendor_by_vendor(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    result = UserController.get_sub_vendor_for_vendor(db_local, request, _user)
    return {"users": result['users'], "permissions": result['permissions']}

@route.post("/create")
@requires_permission('write', ModelNameEnum.SETTING_MODEL.value)
async def create_dub_vendor_by_vendor(request: Request, schema: UserCreateSubVendorSchema, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    return UserController.create_sub_vendor_by_vendor(request, schema, db_local, _user)

@route.put('/update/{id}', response_model=UserSchema | Dict[str, str])
@requires_permission('write', ModelNameEnum.USER_MODEL.value)
async def update_user(id: int, model: UserSchema, request: Request,  db: Session = Depends(get_db), _user: User = Depends(is_authenticated)):
    try:
        if db.in_transaction():
            db.rollback()
        transaction = db.begin()
        user_to_update = db.query(User).filter(User.parent_id == _user.id).filter(User.id == id).first()

        if not user_to_update or (user_to_update.parent_id != _user.id):
            return {"status": False, "message": "Invalid user"}
        
        for field, value in model.dict(exclude_unset=True, exclude={'permissions'}).items():
            setattr(user_to_update, field, value)

        if model.permissions != None:
            user_to_update.permissions.clear()

            for perm_id in model.permissions:
                permission = db.query(Permission).filter(Permission.id == int(perm_id)).first()

                if permission != None: 
                    user_to_update.permissions.append(permission)
                else:
                    continue
                
        db.commit()
        db.refresh(user_to_update)

        return user_to_update
    except Exception as e:
        transaction.rollback()
        return { "status": False, "message": str(e) }
