from datetime import datetime, time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import Request
from App.Enums.OrderEnums import OrderOrderBy, SortOrder
from App.core.auth import LoginController

from App.input_ports.schemas.OrderSchema import OrderResponseModel, OrdersSchema
from App.core.entities.order_repository import IOrderRepository
from App.output_ports.models.CscartModels import CscartOrders

class OrderRepository(IOrderRepository):
    def __init__(self, db_local: Session, db_cscart: Session) -> None:
        super().__init__()
        self.db_local = db_local
        self.db_cscart = db_cscart

    def get_orders(self, request: Request, skip: int, limit: int, status: list,
        start_time: datetime, end_time: datetime, order_by: str, sort_order: str
    ) -> OrderResponseModel:
        user = LoginController.get_current_user_from_cookie(request, self.db_local)

        query = self.db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id)

        # process the status
        if status:
            query = query.filter(CscartOrders.status.in_(status))

        # apply start_time and end_time filter
        if start_time and end_time:
            start_time = datetime.combine(start_time.date(), time.min)
            start_timestamp = int(start_time.timestamp())
            end_time = datetime.combine(end_time.date(), time.max)
            end_timestamp = int(end_time.timestamp())
            query = query.filter(and_(CscartOrders.timestamp >= start_timestamp, CscartOrders.timestamp <= end_timestamp))
        elif start_time:
            start_time = datetime.combine(start_time.date(), time.min)
            start_timestamp = int(start_time.timestamp())
            query = query.filter(CscartOrders.timestamp >= start_timestamp)
        elif end_time:
            end_time = datetime.combine(end_time.date(), time.max)
            end_timestamp = int(end_time.timestamp())
            query = query.filter(CscartOrders.timestamp <= end_timestamp)

        # ordering the result
        if order_by:
            if sort_order == SortOrder.desc.value:
                if order_by == OrderOrderBy.timestamp.value:
                    query = query.order_by(CscartOrders.timestamp.desc())
                elif order_by == OrderOrderBy.status.value:
                    query = query.order_by(CscartOrders.status.desc())
            else:
                if order_by == OrderOrderBy.timestamp.value:
                    query = query.order_by(CscartOrders.timestamp.asc())
                elif order_by == OrderOrderBy.status.value:
                    query = query.order_by(CscartOrders.status.asc())

        total = query.count()
        orders = query.offset(skip).limit(limit).all()
        orders = [OrdersSchema.from_orm(p) for p in orders]
        return {"orders": orders, "total": total}

    def get_order(self, request: Request, order_id: int) -> Optional[OrdersSchema]:
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        query = self.db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id, CscartOrders.order_id == order_id)
        result = query.first()
        return OrdersSchema.from_orm(result)