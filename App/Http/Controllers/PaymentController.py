from sqlalchemy.orm import Session
from fastapi import Request
from Security.Controllers import LoginController
from Database.Models import Payment_method_vendor

class PaymentController:
    def get_payment_method_by_vendor(request: Request, db_local: Session):
        
        user = LoginController.get_current_user_from_cookie(request, db_local)
        payment_method = db_local.query(Payment_method_vendor).filter(Payment_method_vendor.user_id == user.id).all()
        
        return {"user": user, "payment_method": payment_method}

    def update_payment_method_by_vendor(id: int, db_local: Session, db_cscart: Session):
        print("id : ", id)