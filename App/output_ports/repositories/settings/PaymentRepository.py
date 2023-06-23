
import random
import string
from typing import List
from fastapi import HTTPException, status, Request

from sqlalchemy import and_
from App.core.entities.settings.payment_method_repository import IPaymentRepository
from sqlalchemy.orm import Session
from App.input_ports.schemas.Settings.PaymentMethodSchema import PaymentMethodSchema
from App.core.auth.LoginController import get_current_user_from_cookie
from App.core.auth import LoginController
from App.output_ports.models.Models import Payment_method_vendor, User
from fastapi.responses import JSONResponse


class PaymentRepository(IPaymentRepository):
    def __init__(self, db_local: Session):
        self.db_local = db_local
    
    def get_payment_method(self, request: Request) -> List[PaymentMethodSchema]:
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        
        parent = self.db_local.query(User).filter(User.id == user.parent_id).first()
        
        if not parent:
            payment_method = self.db_local.query(Payment_method_vendor).filter(Payment_method_vendor.user_id == user.id).all()
        else:
            payment_method = self.db_local.query(Payment_method_vendor).filter(Payment_method_vendor.user_id == parent.id).all()
        
        return payment_method
    
    # Enable or disable payment method
    def update_payment_method_by_vendor(self, payment_method_id: int, db_local: Session, request: Request):
        _user = get_current_user_from_cookie(request, db=self.db_local)
        payment_method = db_local\
                        .query(Payment_method_vendor)\
                        .filter(Payment_method_vendor.id == payment_method_id)\
                        .filter(Payment_method_vendor.user_id == _user.id)\
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