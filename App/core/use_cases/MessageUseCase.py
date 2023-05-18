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


class MessageUseCase:
    
    def __init__(self, db_local: Session, db_cscart: Session):
        self.message_repository = MessageRepository(db_local, db_cscart)
        self.db_cscart = db_cscart
        self.db_local = db_local
        
    def get_all_message_by_vendor(self, request: Request, skip: int = 0, limit: int = 10):
        _user = get_current_user_from_cookie(request=request, db=self.db_local)
        model_permissions = ModelPermissions(_user)
        
        return self.message_repository.get_all_message_by_vendor(request, skip, limit)
    
    def get_all_message_with_thread(self, request: Request, thread_id: int, db_cscart: Session):
        _user = get_current_user_from_cookie(request=request, db=self.db_local)
        model_permissions = ModelPermissions(_user)
        
        return self.message_repository.get_all_message_with_thread(request, thread_id)
    
    def send_message(self, request: Request, schema: ChatSchema):
        _user = get_current_user_from_cookie(request=request, db=self.db_local)
        
        if not _user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 
        
        model_permissions = ModelPermissions(_user)
        return self.message_repository.send_message(request, schema)