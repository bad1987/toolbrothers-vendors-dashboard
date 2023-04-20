from pydantic import BaseModel
from typing import Text, List, Optional

class CscartUserSchema(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    user_id: Optional[int]
    
    
class MessageSchema(BaseModel):
    thread_id: Optional[int]
    company_id: Optional[str]
    object_id: Optional[str]
    object_type: Optional[str]
    status: Optional[str]
    last_message: Optional[str]
    last_message_user_id: Optional[int]
    last_message_user_type: Optional[str]
    communication_type: Optional[str]
    user_id: Optional[int]
    last_update: Optional[int]
    created_at: Optional[int]
    cscart_users: Optional[CscartUserSchema] = {}
    
    
    def setUser(self, user):
        self.cscart_users = user
        
class ChatSchema(BaseModel):
    thread_id: Optional[int]
    message_id: Optional[int]
    user_id: Optional[int]
    user_type: Optional[str]
    timestamp: Optional[int]
    message: Optional[str]
    cscart_users: Optional[CscartUserSchema] = {}
    
    def setUser(self, user):
        self.cscart_users = user
        
    class Config:
        orm_mode = True


