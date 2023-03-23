from sqlalchemy.orm import Session
from fastapi import Request
from Security.Controllers import LoginController
from Database.CscartModels import CscartOrders

class OrderController:
    def get_orders_by_vendor_connected(request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int):
        
        user = LoginController.get_current_user_from_cookie(request, db_local)

        query = db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id)

        total = query.count()
        orders = query.offset(skip).limit(limit).all()
        
        return {"user": user, "orders": orders, "total": total}