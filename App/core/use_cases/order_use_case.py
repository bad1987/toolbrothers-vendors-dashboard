from datetime import datetime
from typing import List

from fastapi import Depends, Request
from App.Http.Controllers.OrderController import OrderController
from App.core.auth.LoginController import get_current_user_from_cookie
from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel

from App.output_ports.repositories.order_repository import OrderRepository

from sqlalchemy.orm import Session
from App.output_ports.repositories.product_repository import ProductRepository

from App.output_ports.repositories.user_repository import UserRepository


class OrderUsecase:
    def __init__(self, db_local: Session, db_cscart: Session) -> None:
        self.db_local = db_local
        self.db_cscart = db_cscart
        self.order_repository = OrderRepository(db_local=self.db_local, db_cscart=self.db_cscart)
        self.user_repository = UserRepository(self.db_local)
        self.prod_repository = ProductRepository(db_cscart=self.db_cscart, db_local=self.db_local)
    
    def get_order_list(self, request: Request, skip: int, limit: int, 
        status: list, start_time: datetime, end_time: datetime, order_by: str, sort_order: str
    ) -> OrderResponseModel:
        return self.order_repository.get_orders(request=request,skip=skip, limit=limit, 
            status=status, start_time=start_time, end_time=end_time, order_by=order_by, sort_order=sort_order
        )
    
    def get_order(self, request: Request, order_id: int) -> SingleOrderResponseModel:
        result = self.order_repository.get_order(request=request, order_id=order_id)
        return {"order": result}
    
    def get_detail_order(self, request: Request, order_id: int):
  
        result = self.order_repository.get_detail_order(request, order_id)
        return result
    
    def get_orders_by_vendor_connected(self, request: Request, skip: int, limit: int, statuses: list):
        return self.order_repository.get_orders_by_vendor_connected(request, skip, limit, statuses)
