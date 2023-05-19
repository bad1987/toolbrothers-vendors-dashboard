from sqlalchemy.orm import Session
from fastapi import Request, status
from App.core.auth import LoginController
from App.output_ports.models.Models import Payment_method_vendor
from fastapi.responses import JSONResponse
from App.Http.Schema.Settings.PaymentMethodSchema import updatePaymentMethod
from App.output_ports.repositories.payment_repository import PaymentRepository


class PaymentController:

    def __init__(self, db_local: Session) -> None:
        self.db_local = db_local
        self.pay_repo = PaymentRepository(self.db_local)

    def get_payment_method_by_vendor(self, request: Request):
        
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        if user is None:
            return None
        return self.pay_repo.get_payment_method_by_vendor(user.id)


    # Enable or disable payment method
    def update_payment_method_by_vendor(self, request: Request, id: int):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        if user is None:
            return None
        return self.pay_repo.update_payment_method_by_vendor(payment_id=id, user_id=user.id)
    
    # Update credential payment method
    def update_credential_payment_method_by_vendor(self, request: Request, id: int, schema: updatePaymentMethod):
        is_user_authenticate = LoginController.get_current_user_from_cookie(request, self.db_local)
        
        if is_user_authenticate:
            return self.pay_repo.update_credential_payment_method_by_vendor(payment_id=id, user_id=is_user_authenticate.id, schema=schema)