
from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Request
from sqlalchemy.orm import Session

from App.input_ports.schemas.Settings.PaymentMethodSchema import PaymentMethodSchema


class IPaymentRepository(ABC):
    
    def get_payment_method(self, request: Request)->List[PaymentMethodSchema]:
        ...