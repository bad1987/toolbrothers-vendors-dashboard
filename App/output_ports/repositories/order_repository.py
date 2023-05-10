from datetime import datetime, time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import Request
from App.core.auth import LoginController

from App.input_ports.schemas.OrderSchema import OrderResponseModel, OrdersSchema
from App.core.entities.order_repository import IOrderRepository
from App.output_ports.models.CscartModels import CscartOrders

class OrderRepository(IOrderRepository):
    def get_orders(self, request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int, status: str,
        start_time: datetime, end_time: datetime
        ) -> OrderResponseModel:
        user = LoginController.get_current_user_from_cookie(request, db_local)

        query = db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id)

        # process the status
        if status is not None:
            query = query.filter(CscartOrders.status == status)

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

        total = query.count()
        orders = query.offset(skip).limit(limit).all()
        orders = [OrdersSchema.from_orm(p) for p in orders]
        return {"orders": orders, "total": total}

    def get_order(self, request: Request, order_id: int, db_local: Session, db_cscart: Session) -> Optional[OrdersSchema]:
        user = LoginController.get_current_user_from_cookie(request, db_local)
        query = db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id, CscartOrders.order_id == order_id)
        result = query.first()
        return OrdersSchema.from_orm(result)