import re
import time
from fastapi import Depends, HTTPException,Request, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from App.Enums.UserRoleEnum import ModelNameEnum
from App.output_ports.db.Connexion import SessionLocal
from App.output_ports.db.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.PaymentController import PaymentController
from App.output_ports.models.Models import Payment_method
from typing import List
from App.core.Decorators.auth_decorators import requires_permission
from App.core.auth.Acls.RoleChecker import Role_checker
from App.Http.Schema.Settings.PaymentMethodSchema import PaymentMethodSchema, updatePaymentMethod
from fastapi.encoders import jsonable_encoder
from App.core.auth.auth import is_authenticated
from App.core.use_cases.settings.PaymentUseCase import PaymentUseCase


console = Console()


roles_checker = Role_checker()

route = APIRouter(prefix='/payment', tags=['Payment settings'], include_in_schema=False)


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

@route.get("/method", response_model=List[PaymentMethodSchema], responses={200:{"model": PaymentMethodSchema}})
@requires_permission('read', ModelNameEnum.SETTING_MODEL.value)
async def get_payment_method_by_vendor(request: Request, db_local: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    
    payment_use_case = PaymentUseCase(db_local)
    result = payment_use_case.user_repository.get_payment_method(db_local)
    PaymentController.get_payment_method_by_vendor(request, db_local)
    res = []
    for u in result["payment_method"]:
        res.append(PaymentMethodSchema(**jsonable_encoder(u)))
    return res

# Payment method system
@route.get('/method-system')
def payment_method( db_local: Session = Depends(get_db)):
    
    data = [
        {"name": "PayPal", "processor_id": "122"},
        {"name": "PayPal plus", "processor_id": "132"},
        {"name": "Klarna", "processor_id": "134"}
    ]
    
    for item in data:
        payment_methods = Payment_method()
        payment_methods.name = item["name"]
        payment_methods.processor_id = item["processor_id"]
        
        db_local.add(payment_methods)
        db_local.commit()
        
        db_local.flush(payment_methods)

# Enable and disable payment method
@route.get('/update/{id}')
@requires_permission('write', ModelNameEnum.SETTING_MODEL.value)
async def update_payment_method(request: Request, id: int, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated)):
    result = PaymentController.update_payment_method_by_vendor(id, db_local, db_cscart, request) 
    return result

# Update credential payment method
@route.post('/update/credential/{id}')
@requires_permission('write', ModelNameEnum.SETTING_MODEL.value)
async def update_credential_method(request: Request, id: int, schema: updatePaymentMethod, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated)):
    return PaymentController.update_credential_payment_method_by_vendor(request, id, schema, db_local, db_cscart)


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