from typing import List
from fastapi import HTTPException, Request, status
from App.core.Services.SendEmail import send_email
from App.core.auth.Acls.ModelPermissions import ModelPermissions
from App.core.auth.LoginController import get_current_user_from_cookie

from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema, UserSchema
from App.output_ports.repositories.settings.PaymentRepository import PaymentRepository
from sqlalchemy.orm import Session


class PaymentUseCase:
    
    def __init__(self, db: Session):
        self.user_repository = PaymentRepository(db)
        self.db = db