from abc import ABC, abstractmethod

class IPaymentRepository(ABC):
    
    def get_payment_method_by_vendor(self, user_id: int):
        ...

    def update_payment_method_by_vendor(self, payment_id: int, user_id: int):
        ...
    