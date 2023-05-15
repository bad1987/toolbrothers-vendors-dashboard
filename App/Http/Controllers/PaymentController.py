from sqlalchemy.orm import Session
from fastapi import Request, status
from App.core.auth import LoginController
from App.output_ports.models.Models import Payment_method_vendor
from fastapi.responses import JSONResponse
from App.Http.Schema.Settings.PaymentMethodSchema import PaymentMethodSchema, updatePaymentMethod


class PaymentController:
    def get_payment_method_by_vendor(request: Request, db_local: Session):
        
        user = LoginController.get_current_user_from_cookie(request, db_local)
        payment_method = db_local.query(Payment_method_vendor).filter(Payment_method_vendor.user_id == user.id).all()
        return {"payment_method": payment_method}


    # Enable or disable payment method
    def update_payment_method_by_vendor(id: int, db_local: Session, db_cscart: Session, request):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        payment_method = db_local\
                        .query(Payment_method_vendor)\
                        .filter(Payment_method_vendor.id == id)\
                        .filter(Payment_method_vendor.user_id == user.id)\
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
    
    # Update credential payment method
    def update_credential_payment_method_by_vendor(request: Request, id: int, schema: updatePaymentMethod, db_local: Session, db_cscart: Session):
        is_user_authenticate = LoginController.get_current_user_from_cookie(request, db_local)
        
        if is_user_authenticate:
            payment_method = db_local\
                .query(Payment_method_vendor)\
                .filter(Payment_method_vendor.id == id)\
                .filter(Payment_method_vendor.user_id == is_user_authenticate.id)\
                .first()
            if payment_method:
                payment_method.client_secret = schema.client_secret
                payment_method.client_secret_id = schema.client_secret_id
                
                db_local.commit()
                db_local.flush(payment_method)
                
                return JSONResponse(status_code=status.HTTP_201_CREATED, content='Update successful') 
            
            add_payment_credential = Payment_method_vendor()
            add_payment_credential.client_secret = schema.client_secret
            add_payment_credential.client_secret_id = schema.client_secret_id
            
            db_local.add(add_payment_credential)
            db_local.commit()
            db_local.flush(add_payment_credential)
            
            return JSONResponse(status_code=status.HTTP_201_CREATED, content='Created successful') 