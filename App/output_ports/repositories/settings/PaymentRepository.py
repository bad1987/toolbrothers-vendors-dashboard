
import random
import string
from typing import List
from fastapi import HTTPException, status, Request

from sqlalchemy import and_
from App.Enums.LanguageEnum import LanguageEnum
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Http.Schema.UserSchema import UserCreateResponse, UserSchema
from App.core.entities.settings.payment_method_repository import IPaymentRepository
from sqlalchemy.orm import Session
from App.input_ports.schemas.Settings.PaymentMethodSchema import PaymentMethodSchema
from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema
from App.core.auth.LoginController import get_current_user_from_cookie

from App.input_ports.schemas.UserSchema import PermissionSchema, UserSchema
from App.output_ports.models.Models import Permission, User
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

class PaymentRepository(IPaymentRepository):
    def __init__(self, db_cscar: Session):
        self.db_cscart = db_cscar
    
    def get_payment_method(self, request: Request) -> List[PaymentMethodSchema]:
        _user = get_current_user_from_cookie(request, db=self.db)
        return super().get_payment_method()