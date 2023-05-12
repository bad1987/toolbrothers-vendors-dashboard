from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from fastapi import Request

from App.input_ports.schemas.OrderSchema import OrdersSchema

class IOrderRepository(ABC):

    @abstractmethod
    def get_orders(self, request: Request, skip: int, limit: int, 
        status: list, start_time: datetime, end_time: datetime, order_by: str, sort_order: str
    ) -> List[OrdersSchema]:
        ...

    @abstractmethod
    def get_order(self, request: Request, order_id: int) -> Optional[OrdersSchema]:
        ...