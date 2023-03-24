from sqlalchemy.orm import Session
from fastapi import Request, status
from Security.Controllers import LoginController
from Database.Models import Payment_method_vendor
from fastapi.responses import JSONResponse
from Database.CscartModels import Cscart_payments

class PaymentController:
    def get_payment_method_by_vendor(request: Request, db_local: Session):
        
        #user = LoginController.get_current_user_from_cookie(request, db_local)
        payment_method = db_local.query(Payment_method_vendor).filter(Payment_method_vendor.user_id == 3).all()
        return {"payment_method": payment_method}

    def update_payment_method_by_vendor(id: int, db_local: Session, db_cscart: Session):
        payment_method = db_local\
                        .query(Payment_method_vendor)\
                        .filter(Payment_method_vendor.id == id)\
                        .filter(Payment_method_vendor.user_id == 3)\
                        .first()
        
        if not payment_method:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='This payment method not fund!')

        if payment_method.status == "A":
            payment_method.status = "D"
            
            db_local.commit()
            db_local.flush(payment_method)
            return JSONResponse(status_code=status.HTTP_200_OK, content='Status change successful') 
        
        payment_method.status = "A"
        
        db_local.commit()
        db_local.flush(payment_method)
        return JSONResponse(status_code=status.HTTP_200_OK, content='Status change successful') 
        