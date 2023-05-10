from datetime import datetime
from typing import List

from fastapi import Depends, Request
from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel

from App.output_ports.repositories.order_repository import OrderRepository

from sqlalchemy.orm import Session


class OrderUsecase:
    def __init__(self, order_repo:OrderRepository = OrderRepository()) -> None:
        self.order_repository = order_repo
    
    def get_order_list(self, request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int, 
        status: list, start_time: datetime, end_time: datetime, order_by: str, sort_order: str
    ) -> OrderResponseModel:
        return self.order_repository.get_orders(request=request,db_local=db_local,db_cscart=db_cscart,skip=skip, limit=limit, 
            status=status, start_time=start_time, end_time=end_time, order_by=order_by, sort_order=sort_order
        )
    
    def get_order(self, request: Request, order_id: int, db_local: Session, db_cscart: Session) -> SingleOrderResponseModel:
        result = self.order_repository.get_order(request=request,db_local=db_local,db_cscart=db_cscart, order_id=order_id)
        return {"order": result}