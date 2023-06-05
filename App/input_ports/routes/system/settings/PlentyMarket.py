import re
import time
from fastapi import Depends, HTTPException,Request, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from App.Enums.UserRoleEnum import ModelNameEnum
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.PaymentController import PaymentController
from typing import List
from App.core.Decorators.auth_decorators import requires_permission
from App.core.auth.Acls.RoleChecker import Role_checker
from App.Http.Schema.Settings.PlentyMarketSchema import PlentyMarketSchema
from fastapi.encoders import jsonable_encoder
from App.core.auth.auth import is_authenticated
from App.core.use_cases.settings.PaymentUseCase import PaymentUseCase
from App.core.dependencies.db_dependencies import get_db, get_db_cscart
from App.core.auth.auth import validate_token
from App.core.use_cases.settings.PlentyMarketUseCase import PlentyMarketUseCase

console = Console()


roles_checker = Role_checker()

route = APIRouter(prefix='/plenty-market', tags=['Plenty market settings'], include_in_schema=False)


def timestamp_to_date(s):
    return time.ctime(s)


@route.get('/vendor', response_model=List[PlentyMarketSchema], responses={200:{"model": PlentyMarketSchema}})
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_plenty_market_information(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    plenty_market_user_case = PlentyMarketUseCase(db_local)
        
    result = plenty_market_user_case.get_plenty_market_information_by_vendor(request)
    res = []
    for u in result:
        res.append(PlentyMarketSchema(**jsonable_encoder(u)))
    return res

@route.post('/update')
@requires_permission('write', ModelNameEnum.SETTING_MODEL.value)
async def update_or_create(request: Request, schema: PlentyMarketSchema, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    plenty_market_user_case = PlentyMarketUseCase(db_local)
    return plenty_market_user_case.update_or_add_setting_information(request, schema)
