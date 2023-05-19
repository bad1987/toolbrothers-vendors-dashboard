from datetime import datetime
import time
import re
from phpserialize import *
import json
from fastapi import Depends,Request, APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from App.Enums.UserRoleEnum import ModelNameEnum
from App.Http.Controllers.ProductController import ProductController
from sqlalchemy.orm import Session
from rich.console import Console
from fastapi.encoders import jsonable_encoder
from App.Http.Controllers.OrderController import OrderController
from App.core.auth.Acls.RoleChecker import Role_checker
from App.core.Decorators.auth_decorators import requires_permission
from App.core.auth.auth import is_authenticated
from App.core.auth.middlewares.AuthorizationMiddleware import TokenMiddleware
from App.core.dependencies.db_dependencies import get_db, get_db_cscart
from App.core.use_cases.user_use_case import UserUsecase
from App.output_ports.models.Models import User



route = APIRouter(prefix='', tags=['Orders system'], include_in_schema=False)


roles_checker = Role_checker()


@route.get('/orders/list/', response_class=JSONResponse)
@requires_permission('read', ModelNameEnum.ORDER_MODEL.value)
async def get_all_orders(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated), skip: int = 0, limit: int = 10):
    order_cont = OrderController(db_local=db_local, db_cscart=db_cscart)
    result = order_cont.get_orders_by_vendor_connected(request, skip, limit)
    return {'orders': result["orders"], 'total': result["total"]}

@route.get('/orders/stats')
@requires_permission('read', ModelNameEnum.ORDER_MODEL.value)
async def get_orders_stats(request: Request, start_date: str, end_date: str, db_cscart: Session = Depends(get_db_cscart), db_local: Session = Depends(get_db), _user: User = Depends(is_authenticated)):
    start_date_string = f"{start_date} 00:00:00"
    end_date_string = f"{end_date} 23:59:59"
    company_id=_user.company_id

    if (company_id == None and _user.parent_id != None):
        parent = db_local.query(User).filter(User.id == _user.parent_id).first()

        company_id = parent.company_id
    order_cont = OrderController(db_local=db_local, db_cscart=db_cscart)
    res = order_cont.get_order_stats(start_date_string, end_date_string, company_id)
    p_res = ProductController.get_product_stats(db_cscart, company_id)

    # Chart data
    chart_datas = order_cont.get_grouped_orders(start_date, end_date, company_id)

    res.update(p_res)
    res.update({ "chart_datas": chart_datas })

    res.update(p_res)

    # dealing with the previous period
    prev_period = order_cont.get_previous_interval([start_date, end_date])
    p_stats = order_cont.get_order_stats(prev_period[0], prev_period[1], company_id)
    p_chart_datas = order_cont.get_grouped_orders(prev_period[0], prev_period[1], company_id)
    p_stats.update({
        'percent_income': order_cont.progression_percentage(res['income'], p_stats['income']),
        'percent_sales': order_cont.progression_percentage(res['sales'], p_stats['sales']),
        'percent_orders': order_cont.progression_percentage(res['orders'], p_stats['orders']),
        'label': "previous period",
        'prev_chart': p_chart_datas
    })
    res.update({
        'prev_period': p_stats
    })
    res.update({
        'start_date': start_date,
        'end_date': end_date
    })
    return res