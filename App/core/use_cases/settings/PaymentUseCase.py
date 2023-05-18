from typing import List
from fastapi import HTTPException, Request, status
from App.core.Services.SendEmail import send_email
from App.core.auth.Acls.ModelPermissions import ModelPermissions
from App.core.auth.LoginController import get_current_user_from_cookie
from App.input_ports.schemas.Settings.PaymentMethodSchema import PaymentMethodSchema

from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema, UserSchema
from App.output_ports.repositories.settings.PaymentRepository import PaymentRepository
from sqlalchemy.orm import Session


class PaymentUseCase:
    
    def __init__(self, db_local: Session):
        self.payment_repository = PaymentRepository(db_local)
        self.db_local = db_local
        
    def get_payment_method(self, request: Request)->PaymentMethodSchema:
        _user = get_current_user_from_cookie(request=request, db=self.db_local)
        model_permissions = ModelPermissions(_user)
        
        return self.payment_repository.get_payment_method(request)
    
    def update_payment_method(self, request: Request, payment_method_id: int):
        _user = get_current_user_from_cookie(request, self.db_local)
        model_permissions = ModelPermissions(_user)
        
        return self.payment_repository.update_payment_method_by_vendor(payment_method_id, self.db_local, request)
        