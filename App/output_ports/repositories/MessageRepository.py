
from datetime import datetime
import random
import string
from typing import List
from fastapi import HTTPException, status, Request

from sqlalchemy import and_
from App.core.Services.SendEmail import send_email
from App.core.entities.IMessageRepository import ImessageRepository
from sqlalchemy.orm import Session
from App.core.auth.LoginController import get_current_user_from_cookie
from App.core.auth import LoginController
from fastapi.responses import JSONResponse
from App.input_ports.schemas.MessageSchema import ChatSchema
from App.output_ports.models.CscartModels import Cscart_vendor_communication_messages, Cscart_vendor_communications, CscartUsers


class MessageRepository(ImessageRepository):
    def __init__(self, db_local: Session, db_cscart: Session):
        self.db_local = db_local
        self.db_cscart = db_cscart
        
    def get_all_message_by_vendor(self, request: Request, skip: int = 0, limit: int = 10):
        _user = get_current_user_from_cookie(request, db=self.db_local)
        
        if not _user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied')
         
        query = self.db_cscart.query(Cscart_vendor_communications)\
        .join(CscartUsers, CscartUsers.user_id == Cscart_vendor_communications.user_id)\
        .filter(Cscart_vendor_communications.company_id == _user.company_id)\
        .order_by(Cscart_vendor_communications.last_updated.desc())\
                    
        total = query.count()
        messages = query.offset(skip).limit(limit)\
            .add_columns(CscartUsers)\
            .all()
        
        return {"messages": messages, "total": total}
    
    def get_all_message_with_thread(self, request: Request, thread_id: int):
        _user = get_current_user_from_cookie(request, db=self.db_local)
        
        if not _user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied')
        
        query = self.db_cscart.query(Cscart_vendor_communication_messages)\
            .join(Cscart_vendor_communications, Cscart_vendor_communications.thread_id == Cscart_vendor_communication_messages.thread_id)\
            .join(CscartUsers, CscartUsers.user_id == Cscart_vendor_communication_messages.user_id)\
            .filter(Cscart_vendor_communication_messages.thread_id == thread_id)\
            .filter(Cscart_vendor_communications.company_id == _user.company_id)\
            .add_columns(CscartUsers)\
            .all()
        
        return query

    def send_message(self, request: Request, chatSchema: ChatSchema):
        print("dzfczdec", chatSchema)
        _user = get_current_user_from_cookie(request, db=self.db_local)
        
        if not _user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 
        
        last_message = self.db_cscart.query(Cscart_vendor_communications)\
        .filter(Cscart_vendor_communications.company_id == _user.company_id)\
        .filter(Cscart_vendor_communications.thread_id == chatSchema.thread_id)\
        .first()
        
        if last_message:
            last_message.last_message = chatSchema.message[:200]
            last_message.thread_id = chatSchema.thread_id
            last_message.company_id = _user.company_id
            last_message.status = "N"
            last_message.user_id = chatSchema.user_id
            last_message.storefront_id = 1
            last_message.object_type = "P"
            last_message.last_updated = datetime.timestamp(datetime.now())
            
            self.db_cscart.commit()
            self.db_cscart.flush(last_message)
            
            message = MessageRepository.persist_message(chatSchema)
            message.user_id = chatSchema.user_id
            message.user_id = _user.user_id
            
            self.db_cscart.add(message)
            self.db_cscart.commit()
            self.db_cscart.flush(message)
            
            send_email("mafobruno990@gmail.com", "New message TOOLBROTHERS", f"Hello, {_user.firstname} your have new message on TOOLBROTHERS, please click this link for read message.")
            
            return JSONResponse(status_code=status.HTTP_201_CREATED, content='Create successful !!')  
            
        # last_new_message = Cscart_vendor_communications()
        
        # last_new_message.thread_id = chatSchema.thread_id
        # last_new_message.company_id = _user.company_id
        # last_new_message.last_message = chatSchema.message[:200]
        # last_new_message.status = "N"
        # last_new_message.user_id = chatSchema.user_id
        # last_new_message.storefront_id = 1
        # last_new_message.object_type = "P"
        
        # self.db_cscart.add(last_new_message)
        # self.db_cscart.commit()
        # self.db_cscart.flush(last_new_message)
        # last_message.last_updated = datetime.timestamp(datetime.now())
        
        # last_message.user_id = chatSchema.user_id
        # self.db_cscart.commit()
        # self.db_cscart.flush(last_message)
        
        # message = self.persist_message(chatSchema)
        
        # self.db_cscart.add(message)
        # self.db_cscart.commit()
        # self.db_cscart.flush(message)
        
        # send_email("mafobruno990@gmail.com", "New message Dinotech", f"Hello, {_user.firstname} your have new message on Dinotech, please click this link for read message.")
        
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Last message not found !!')  
        
        
    def persist_message(schema):
        message = Cscart_vendor_communication_messages()
        message.thread_id = schema.thread_id
        if schema.role == "Role_direct_sale" or schema.role == "Role_affiliate": 
            message.user_type = "V"
        else:
            if schema.role == "Role_admin":
                message.user_type = "A"
            else:
                message.user_type = "C"
        
        message.message = schema.message
        message.timestamp = datetime.timestamp(datetime.now())
        
        return message
        
              