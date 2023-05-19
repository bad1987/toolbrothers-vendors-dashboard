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
from App.core.use_cases.settings.SettingUseCase import SettingUseCase

console = Console()


roles_checker = Role_checker()

route = APIRouter(prefix='/setting', tags=['Get token api from user'], include_in_schema=False)


def timestamp_to_date(s):
    return time.ctime(s)


@route.get('/api-token-user')
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def generate_token_for_api(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    use_case = SettingUseCase(db_local)
    return use_case.generate_token_for_api(request)
    

@route.get('/get-token-api')
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_token_for_api(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    use_case = SettingUseCase(db_local)
    return use_case.get_token_api(request)