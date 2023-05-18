from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Request
from sqlalchemy.orm import Session
from App.input_ports.schemas.MessageSchema import ChatSchema

from App.input_ports.schemas.Settings.PaymentMethodSchema import PaymentMethodSchema


class ImessageRepository(ABC):
    
    def get_all_message_by_vendor(self, request: Request, skip: int = 0, limit: int = 10):
        ...
        
    def get_all_message_with_thread(self, request: Request, thread_id: int):
        ...
        
    def send_message(self, request, Request, chatSchema: ChatSchema):
        ...