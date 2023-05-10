from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session

from fastapi import Request

from App.input_ports.schemas.OrderSchema import OrdersSchema

class IOrderRepository(ABC):

    @abstractmethod
    def get_orders(self, request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int) -> List[OrdersSchema]:
        ...

    @abstractmethod
    def get_order(self, request: Request, db_local: Session, db_cscart: Session) -> Optional[OrdersSchema]:
        ...