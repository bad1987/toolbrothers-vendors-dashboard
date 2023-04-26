from datetime import datetime
import time
from fastapi import Depends,Request, APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from App.Enums.UserRoleEnum import ModelNameEnum
from App.Http.Controllers.ProductController import ProductController
from Decorators.auth_decorators import requires_permission, requires_vendor_access
from Routes.Users import is_authenticated
from Security.Acls.RoleChecker import Role_checker
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
@requires_permission('read', ModelNameEnum.ORDER_MODEL.value)
async def get_all_orders(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated), skip: int = 0, limit: int = 10):
    result = OrderController.get_orders_by_vendor_connected(request, db_local, db_cscart, skip, limit)
    return {'orders': result["orders"], 'total': result["total"]}

@route.get('/orders/stats')
@requires_permission('read', ModelNameEnum.ORDER_MODEL.value)
async def get_orders_stats(request: Request, start_date: str, end_date: str, db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated)):
    start_date_string = f"{start_date} 00:00:00"
    end_date_string = f"{end_date} 23:59:59"
    company_id=_user.company_id

    res = OrderController.get_order_stats(db_cscart, start_date_string, end_date_string, company_id)
    p_res = ProductController.get_product_stats(db_cscart, company_id)

    # Chart datas
    chart_datas = OrderController.get_grouped_orders(db_cscart, _user, start_date, end_date)

    res.update(p_res)
    res.update({ "chart_datas": chart_datas })

    res.update(p_res)
    prev_period = OrderController.get_previous_interval([start_date, end_date])
    p_stats = OrderController.get_order_stats(db_cscart, prev_period[0], prev_period[1], company_id)
    p_stats.update({
        'percent_income': OrderController.progression_percentage(res['income'], p_stats['income']),
        'percent_sales': OrderController.progression_percentage(res['sales'], p_stats['sales']),
        'percent_orders': OrderController.progression_percentage(res['orders'], p_stats['orders']),
        'label': "previous period"
    })
    res.update({
        'prev_period': p_stats
    })
    return res

@route.get('/orders/grouped')
async def get_grouped_orders(request: Request, db_cscart: Session = Depends(get_db_cscart), db_local: Session = Depends(get_db)):
    user = LoginController.get_current_user_from_cookie(request, db_local)

    orders = OrderController.get_grouped_orders(db_cscart, user)

    return orders
