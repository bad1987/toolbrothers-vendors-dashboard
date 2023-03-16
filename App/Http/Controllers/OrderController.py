from sqlalchemy.orm import Session
from fastapi import Request
from Security.Controllers import LoginController
from Database.CscartModels import CscartOrders

class OrderController:
    def get_orders_by_vendor_connected(request: Request, db_local: Session, db_cscart: Session):
        
        user = LoginController.get_current_user_from_cookie(request, db_local)
        orders = db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id).all()
        
        return {"user": user, "orders": orders}