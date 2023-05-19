from typing import List
from fastapi import HTTPException, Request, status
from App.core.Services.SendEmail import send_email
from App.core.auth.Acls.ModelPermissions import ModelPermissions
from App.core.auth.LoginController import get_current_user_from_cookie
from App.core.entities.IMessageRepository import ImessageRepository
from App.input_ports.schemas.Settings.PaymentMethodSchema import PaymentMethodSchema

from App.input_ports.schemas.UserSchema import PermissionSchema, UserCreateSchema, UserSchema
from App.output_ports.repositories.MessageRepository import MessageRepository
from App.output_ports.repositories.settings.PaymentRepository import PaymentRepository
from App.input_ports.schemas.MessageSchema import ChatSchema
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from App.output_ports.repositories.settings.SettingRepository import SettingRepository


class SettingUseCase:
    
    def __init__(self, db_local: Session):
        self.settingRepository = SettingRepository(db_local)
        self.db_local = db_local
        
    def generate_token_for_api(self, request: Request):
        return self.settingRepository.generate_token_for_api(request)
    
    def get_token_api(self, request: Request):
        return self.settingRepository.get_token_api(request)