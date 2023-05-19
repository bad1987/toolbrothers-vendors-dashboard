
from fastapi import Request, status
from fastapi.responses import JSONResponse
from App.Http.Schema.Settings.PaymentMethodSchema import updatePaymentMethod
from App.core.entities.payment_repository import IPaymentRepository
from sqlalchemy.orm import Session

from App.output_ports.models.Models import Payment_method_vendor

class PaymentRepository(IPaymentRepository):
    def __init__(self, db_local: Session) -> None:
        super().__init__()
        self.db_local = db_local
    
    def get_payment_method_by_vendor(self, user_id: int):
        payment_method = self.db_local.query(Payment_method_vendor).filter(Payment_method_vendor.user_id == user_id).all()
        return {"payment_method": payment_method}
    
    def update_payment_method_by_vendor(self, payment_id: int, user_id: int):
        payment_method = self.db_local\
            .query(Payment_method_vendor)\
            .filter(Payment_method_vendor.id == payment_id)\
            .filter(Payment_method_vendor.user_id == user_id)\
            .first()
        
        if not payment_method:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='This payment method not fund!')

        if payment_method.status == "A":
            payment_method.status = "D"
            
            self.db_local.commit()
            self.db_local.flush(payment_method)
            return JSONResponse(status_code=status.HTTP_200_OK, content='Status change successful') 
        
        payment_method.status = "A"
        
        self.db_local.commit()
        self.db_local.flush(payment_method)
        return JSONResponse(status_code=status.HTTP_200_OK, content='Status change successful') 
    

    def update_credential_payment_method_by_vendor(self, payment_id: int, user_id: int, schema: updatePaymentMethod):
        payment_method = self.db_local\
            .query(Payment_method_vendor)\
            .filter(Payment_method_vendor.id == payment_id)\
            .filter(Payment_method_vendor.user_id == user_id)\
            .first()
        if payment_method:
            payment_method.client_secret = schema.client_secret
            payment_method.client_secret_id = schema.client_secret_id
            
            self.db_local.commit()
            self.db_local.flush(payment_method)
            
            return JSONResponse(status_code=status.HTTP_201_CREATED, content='Update successful') 
        
        add_payment_credential = Payment_method_vendor()
        add_payment_credential.client_secret = schema.client_secret
        add_payment_credential.client_secret_id = schema.client_secret_id
        
        self.db_local.add(add_payment_credential)
        self.db_local.commit()
        self.db_local.flush(add_payment_credential)
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Created successful')