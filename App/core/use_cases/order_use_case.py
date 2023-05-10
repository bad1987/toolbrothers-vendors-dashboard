from typing import List

from fastapi import Depends, Request
from App.input_ports.schemas.OrderSchema import OrderResponseModel

from App.output_ports.repositories.order_repository import OrderRepository

from sqlalchemy.orm import Session


class OrderUsecase:
    def __init__(self, order_repo:OrderRepository = OrderRepository()) -> None:
        self.order_repository = order_repo
    
    def get_order_list(self, request: Request, db_local: Session, db_cscart: Session, skip: int = 0, limit: int = 10) -> OrderResponseModel:
        return self.order_repository.get_orders(request=request,db_local=db_local,db_cscart=db_cscart,skip=skip, limit=limit)