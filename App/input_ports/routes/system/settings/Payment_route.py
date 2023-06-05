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
from App.Http.Schema.Settings.PaymentMethodSchema import PaymentMethodSchema, updatePaymentMethod
from fastapi.encoders import jsonable_encoder
from App.core.auth.auth import is_authenticated
from App.core.use_cases.settings.PaymentUseCase import PaymentUseCase
from App.core.dependencies.db_dependencies import get_db, get_db_cscart
from App.core.auth.auth import validate_token

console = Console()


roles_checker = Role_checker()

route = APIRouter(prefix='/payment', tags=['Payment settings'], include_in_schema=False)


def timestamp_to_date(s):
    return time.ctime(s)

@route.get("/method", response_model=List[PaymentMethodSchema], responses={200:{"model": PaymentMethodSchema}})
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_payment_method_by_vendor(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    
    payment_use_case = PaymentUseCase(db_local)
    result = payment_use_case.get_payment_method(request)
    # PaymentController.get_payment_method_by_vendor(request, db_local)
    res = []
    for u in result:
        res.append(PaymentMethodSchema(**jsonable_encoder(u)))
    return res

# Enable and disable payment method
@route.get('/update/{payment_method_id}')
@requires_permission('write', ModelNameEnum.SETTING_MODEL.value)
async def update_payment_method(request: Request, payment_method_id: int, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    payment_use_case = PaymentUseCase(db_local)
    return payment_use_case.update_payment_method(request, payment_method_id)

# Update credential payment method
@route.post('/update/credential/{id}')
@requires_permission('write', ModelNameEnum.SETTING_MODEL.value)
async def update_credential_method(request: Request, id: int, schema: updatePaymentMethod, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated), payload: dict = Depends(validate_token)):
    pay_cont = PaymentController(db_local=db_local)
    return pay_cont.update_credential_payment_method_by_vendor(request=request, id=id, schema=schema)

# Modify secret credential
def extract_credentials(payload: str):
    if not payload:
        return None
    regex = '^.*?"username".*?"(.*?)".*?"password".*?"(.*?)"'
    res = re.findall(regex, payload)
    if len(res) and isinstance(res[0], tuple):
        return {
            'username': res[0][0],
            'password': res[0][1],
        }
    regex = '^.*?"client_id".*?"(.*?)".*?"secret".*?"(.*?)"'
    res = re.findall(regex, payload)
    if len(res) and isinstance(res[0], tuple):
        return {
            'username': res[0][0],
            'password': res[0][1],
        }
    return None