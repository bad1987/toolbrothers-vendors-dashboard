from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request
from App.Enums.OrderEnums import OrderOrderBy, OrderStatus, SortOrder
from App.core.auth.auth import validate_token
from App.core.use_cases.order_use_case import OrderUsecase

from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel
from App.output_ports.db.Connexion import SessionLocal
from App.output_ports.db.CscartConnexion import CscartSession
from sqlalchemy.orm import Session

from App.utils.datetime_utils import validate_end_time, validate_start_time

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

api_route = APIRouter(prefix='/api', tags=['Orders system'], include_in_schema=True)

@api_route.get('/orders/list/', response_model=OrderResponseModel)
async def get_orders_list(request: Request, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), 
    payload: dict = Depends(validate_token), page: int = 1, items_per_page: int = 10,
    status: List[OrderStatus] = Query([], description="The status of the orders to search for. Possible values are: P—processed, C—complete, O—open, F—failed, D—declined, B—backordered, I—cancelled, Y—awaiting call"), 
    start_time: Optional[datetime] = Depends(validate_start_time), 
    end_time: Optional[datetime] = Depends(validate_end_time),
    order_by: Optional[OrderOrderBy] = Query(
        None,
        description="The column to order the results by. Possible values are defined by the OrderOrderBy enum."
    ),
    sort_order: Optional[SortOrder] = Query(
        SortOrder.asc,
        description="The sort order of the results. Possible values are: asc (ascending), desc (descending)"
    )
):
    order_usecase = OrderUsecase()
    skip = (page - 1) * items_per_page
    limit = items_per_page
    status = [s.value for s in status]
    if order_by is not None:
        order_by = order_by.value
    sort_order = sort_order.value

    result = order_usecase.get_order_list(request=request, db_cscart=db_cscart, db_local=db_local,skip=skip, limit=limit,
        status=status, start_time=start_time, end_time=end_time, order_by=order_by, sort_order=sort_order
    )
    return result

@api_route.get('/order/', response_model=SingleOrderResponseModel)
async def get_order(request: Request, order_id: int, db_local: Session = Depends(get_db), db_cscart: Session = Depends(get_db_cscart), payload: dict = Depends(validate_token)):
    order_usecase = OrderUsecase()
    result = order_usecase.get_order(request=request, db_cscart=db_cscart, db_local=db_local, order_id=order_id)
    return result