from typing import List, Optional
from sqlalchemy.orm import Session

from fastapi import Request
from App.core.auth import LoginController

from App.input_ports.schemas.OrderSchema import OrderResponseModel, OrdersSchema
from App.core.entities.order_repository import IOrderRepository
from App.output_ports.models.CscartModels import CscartOrders

class OrderRepository(IOrderRepository):
    def get_orders(self, request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int) -> OrderResponseModel:
        user = LoginController.get_current_user_from_cookie(request, db_local)

        query = db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id)

        total = query.count()
        orders = query.offset(skip).limit(limit).all()
        orders = [OrdersSchema.from_orm(p) for p in orders]
        return {"orders": orders, "total": total}

    def get_order(self, request: Request, db_local: Session, db_cscart: Session) -> Optional[OrdersSchema]:
        ...