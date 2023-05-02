from pydantic import BaseModel
from typing import Text, List, Optional

class PaymentMethodSchema(BaseModel):
    id: int
    name: Optional[str]
    processor_id: Optional[str]
    status: Optional[str]
    client_secret: Optional[str]
    client_secret_id: Optional[str]
    
class updatePaymentMethod(BaseModel):
    client_secret: Optional[str]
    client_secret_id: Optional[str]
    