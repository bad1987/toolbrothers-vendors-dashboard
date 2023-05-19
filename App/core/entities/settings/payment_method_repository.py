
from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Request
from sqlalchemy.orm import Session

from App.input_ports.schemas.Settings.PaymentMethodSchema import PaymentMethodSchema


class IPaymentRepository(ABC):
    
    def get_plenty_market_information_by_vendor(self, request: Request)->List[PaymentMethodSchema]:
        ...
    
    def update_or_add_setting_information(self, request: Request, payment_method_id: int):
        ...