from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text
from fastapi import Request, status, HTTPException
from Security.Controllers import LoginController
from Database.CscartModels import CscartUsers, Cscart_vendor_communications, Cscart_vendor_communication_messages
from fastapi.responses import JSONResponse
from schemas.Settings.PlentyMarketSchema import PlentyMarketSchema
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
            .filter(Cscart_vendor_communication_messages.user_id == user_id)\
            .filter(Cscart_vendor_communications.company_id == user.company_id)\
            .add_columns(CscartUsers)\
            .all()
        
        console.log(query)
        return query