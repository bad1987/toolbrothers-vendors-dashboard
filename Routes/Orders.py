import time
from fastapi import Depends,Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from Security.Controllers import LoginController
from Security.DTO.UserDto import UserDtoCreate
from Database.Connexion import SessionLocal
from Database.CscartConnexion import CscartSession
from sqlalchemy.orm import Session
from rich.console import Console
from App.Http.Controllers.OrderController import OrderController

console = Console()



route = APIRouter(prefix='')
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

@route.get("/orders", response_class=HTMLResponse)
async def get_order_by_vendor(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart)):

    result = OrderController.get_orders_by_vendor_connected(request, db_local, db_cscart)
    context = {
        "request": request,
        "orders": result["orders"],
        "user": result["user"]
    }
    
    return templates.TemplateResponse("orders/index.html", context) 

@route.get('/orders/list/', response_class=JSONResponse)
async def get_all_orders(request: Request, db_local: Session = Depends(get_db),
                          db_cscart: Session = Depends(get_db_cscart), skip: int = 0, limit: int = 10):
    result = OrderController.get_orders_by_vendor_connected(request, db_local, db_cscart, skip, limit)

    return {'orders': result["orders"], 'total': result["total"]}