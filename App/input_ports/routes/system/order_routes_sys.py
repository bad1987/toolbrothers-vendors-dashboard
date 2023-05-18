from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request
from App.Enums.OrderEnums import OrderOrderBy, OrderStatus, SortOrder
from App.core.auth.auth import is_authenticated, validate_token
from App.core.dependencies.db_dependencies import get_db, get_db_cscart
from App.core.use_cases.order_use_case import OrderUsecase

from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel
from sqlalchemy.orm import Session

from App.utils.datetime_utils import validate_end_time, validate_start_time

sys_route = APIRouter(prefix='', tags=['Orders system'], include_in_schema=True)

@sys_route.get('/orders/list/', response_model=OrderResponseModel)
async def get_orders_list(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated), skip: int = 0, limit: int = 10):
    order_usecase = OrderUsecase(db_local=db_local, db_cscart=db_cscart)
    result = order_usecase.get_orders_by_vendor_connected(request, skip, limit)
    
    return {'orders': result["orders"], 'total': result["total"]}

@sys_route.get('/order/detail/{order_id}')
async def get_detail_order(request: Request, order_id: int, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart)):
    order_usecase = OrderUsecase(db_local=db_local, db_cscart=db_cscart)
    result = order_usecase.get_detail_order(request, order_id)
    
    return result