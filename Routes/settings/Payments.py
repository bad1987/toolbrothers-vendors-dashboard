import time
from fastapi import Depends,Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.PaymentController import PaymentController
from Database.Models import Payment_method
from typing import List
from schemas.Payment_method.PaymentMethodSchema import PaymentMethodSchema
from fastapi.encoders import jsonable_encoder
from Routes.Users import is_authenticated

console = Console()



route = APIRouter(prefix='/payment')
templates = Jinja2Templates(directory="templates")


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
def get_payment_method_by_vendor(request: Request, db_local: Session = Depends(get_db)):
    result = PaymentController.get_payment_method_by_vendor(request, db_local)
    res = []
    console.log(result)
    
    for u in result["payment_method"]:
        res.append(PaymentMethodSchema(**jsonable_encoder(u)))
    return res
    # context = {
    #     "request": request,
    #     "payment_method": result["payment_method"],
    #     "user": result["user"]
    # }
    
    # return templates.TemplateResponse("Settings/payment_method.html", context)

# Payment method system
@route.get('/method-system')
def payment_method(db_local: Session = Depends(get_db)):
    
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
def update_payment_method(id: int, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart)):
    console.log(id)
    result = PaymentController.update_payment_method_by_vendor(id, db_local, db_cscart)
    
    return result

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