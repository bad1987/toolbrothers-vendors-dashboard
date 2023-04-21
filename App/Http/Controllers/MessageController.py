from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text
from fastapi import Request, status, HTTPException
from Security.Controllers import LoginController
from Database.CscartModels import CscartUsers, Cscart_vendor_communications, Cscart_vendor_communication_messages
from fastapi.responses import JSONResponse
from App.Http.Schema.MessageSchema import ChatSchema
from rich.console import Console
console = Console()

class MessageController:
    def get_last_message(request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 
        query = db_cscart.query(Cscart_vendor_communications)\
        .join(CscartUsers, CscartUsers.user_id == Cscart_vendor_communications.user_id)\
        .filter(Cscart_vendor_communications.company_id == user.company_id)\
        .order_by(Cscart_vendor_communications.created_at.desc())\
                    
        total = query.count()
        messages = query.offset(skip).limit(limit)\
            .add_columns(CscartUsers)\
            .all()
        
        return {"messages": messages, "total": total}
    
    def get_all_message_with_thread(request: Request, thread_id: int, user_id: int, db_local: Session, db_cscart: Session):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 

        query = db_cscart.query(Cscart_vendor_communication_messages)\
            .join(Cscart_vendor_communications, Cscart_vendor_communications.thread_id == Cscart_vendor_communication_messages.thread_id)\
            .join(CscartUsers, CscartUsers.user_id == Cscart_vendor_communications.user_id)\
            .filter(Cscart_vendor_communication_messages.thread_id == thread_id)\
            .filter(Cscart_vendor_communications.company_id == user.company_id)\
            .add_columns(CscartUsers)\
            .all()
        
        console.log(query)
        return query
    
    def send_message(request: Request, chatSchema: ChatSchema, db_local: Session, db_cscart: Session):
        user = LoginController.get_current_user_from_cookie(request, db_local)
        
        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 
        
        last_message = db_cscart.query(Cscart_vendor_communications)\
        .filter(Cscart_vendor_communications.company_id == user.company_id)\
        .filter(Cscart_vendor_communications.thread_id == chatSchema.thread_id)\
        .first()
        
        if last_message:
            last_message.last_message = chatSchema.message
            last_message.thread_id = chatSchema.thread_id
            last_message.company_id = user.company_id
            last_message.status = "N"
            last_message.user_id = chatSchema.user_id
            last_message.storefront_id = 1
            last_message.object_type = "P"
            
            db_cscart.commit()
            db_cscart.flush(last_message)
            
            message = MessageController.persist_message(chatSchema, user.roles)
            message.user_id = chatSchema.user_id
            
            db_cscart.add(message)
            db_cscart.commit()
            db_cscart.flush(message)
            
            return JSONResponse(status_code=status.HTTP_201_CREATED, content='Create successful !!')  
            

        last_new_message = Cscart_vendor_communications()
        
        last_message.last_message = chatSchema.message
        last_message.thread_id = chatSchema.thread_id
        last_message.company_id = user.company_id
        last_message.status = "N"
        last_message.user_id = chatSchema.user_id
        last_message.storefront_id = 1
        last_message.object_type = "P"
        
        db_cscart.add(last_new_message)
        db_cscart.commit()
        db_cscart.flush(last_new_message)
        
        message.user_id = chatSchema.user_id
        db_cscart.commit()
        db_cscart.flush(last_message)
        
        message = MessageController.persist_message(chatSchema, user.roles)
        
        db_cscart.add(message)
        db_cscart.commit()
        db_cscart.flush(message)
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Create successful !!')  
        
        
    def persist_message(schema: ChatSchema, role: str):
        message = Cscart_vendor_communication_messages()
        console.log(role)
        message.thread_id = schema.thread_id
        if role == "UserRoleEnum.ADMIN": message.user_type = "A"
        if role == "UserRoleEnum.DIRECT_SALE": message.user_type = "V"
        if role == "UserRoleEnum.DIRECT_AFFILIATE": message.user_type = "V"
        if role == "UserRoleEnum.DIRECT_SUB_VENDOR": message.user_type = "V"
        if role != "UserRoleEnum.ADMIN" and role != "UserRoleEnum.DIRECT_SALE" and role != "UserRoleEnum.DIRECT_AFFILIATE" and role != "UserRoleEnum.DIRECT_SUB_VENDOR": message.user_type = "C"
        
        message.message = schema.message
        
        
        return message
        
              
            