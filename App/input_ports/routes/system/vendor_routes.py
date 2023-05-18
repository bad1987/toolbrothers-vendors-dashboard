import re
import time
from fastapi import Depends, Request, APIRouter
from App.Enums.UserRoleEnum import ModelNameEnum
from sqlalchemy.orm import Session
from rich.console import Console
from typing import Dict, List
from App.Http.Schema.UserSchema import UserCreateSubVendorSchema, UserSchema
from App.Http.Controllers.UserController import UserController
from App.core.auth.Acls.RoleChecker import Role_checker
from App.core.Decorators.auth_decorators import requires_permission
from App.core.auth.auth import is_authenticated

from App.core.auth.middlewares.AuthorizationMiddleware import TokenMiddleware
from App.core.dependencies.db_dependencies import get_db, get_db_cscart
from App.input_ports.schemas.UserSchema import PermissionReturnModel, UserListSchema
from App.output_ports.models.Models import User


roles_checker = Role_checker()

route = APIRouter(prefix='/sub-vendor', tags=['Handle sub vendor'], include_in_schema=False)


@route.get("/get", response_model=UserListSchema)
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
    return UserController.update_subvendor(model, db, _user)


