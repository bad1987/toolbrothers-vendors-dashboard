from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request
from App.Enums.OrderEnums import OrderOrderBy, OrderStatus, SortOrder
from App.Enums.UserRoleEnum import ModelNameEnum
from App.core.Decorators.auth_decorators import requires_permission
from App.Enums.ProductEnums import ProductStatus
from App.core.auth.auth import is_authenticated, validate_token
from App.core.dependencies.db_dependencies import get_db, get_db_cscart
from App.core.use_cases.order_use_case import OrderUsecase

from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel
from sqlalchemy.orm import Session

from App.utils.datetime_utils import validate_end_time, validate_start_time
from App.output_ports.models.Models import User

sys_route = APIRouter(prefix='', tags=['Orders system'], include_in_schema=False)

@sys_route.get('/orders/list', response_model=OrderResponseModel)
@requires_permission('read', ModelNameEnum.ORDER_MODEL.value)
async def get_orders_list(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), _user: dict = Depends(is_authenticated), skip: int = 0, limit: int = 10,
    statuses: List[OrderStatus] = Query([OrderStatus.AWAITING_CALL.value, OrderStatus.BACKORDERED.value, OrderStatus.CANCELLED.value, OrderStatus.COMPLETE.value, OrderStatus.DECLINED.value, OrderStatus.FAILED.value, OrderStatus.OPEN.value, OrderStatus.PROCESSED.value])                          
):
    order_usecase = OrderUsecase(db_local=db_local, db_cscart=db_cscart)
    statuses = [status.value for status in statuses]
    result = order_usecase.get_orders_by_vendor_connected(request, skip, limit, statuses)
    
    return {'orders': result["orders"], 'total': result["total"]}

@sys_route.get('/order/detail/{order_id}')
async def get_detail_order(request: Request, order_id: int, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart)):
    order_usecase = OrderUsecase(db_local=db_local, db_cscart=db_cscart)
    result = order_usecase.get_detail_order(request, order_id)
    
    return result

@sys_route.get('/orders/stats')
@requires_permission('read', ModelNameEnum.ORDER_MODEL.value)
async def get_orders_stats(request: Request, start_date: str, end_date: str, db_cscart: Session = Depends(get_db_cscart), db_local: Session = Depends(get_db), _user: User = Depends(is_authenticated)):
    order_usecase = OrderUsecase(db_local=db_local, db_cscart=db_cscart)
    return order_usecase.get_order_statistics(request=request,start_date=start_date, end_date=end_date)
