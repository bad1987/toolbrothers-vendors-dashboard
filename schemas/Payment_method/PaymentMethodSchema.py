from pydantic import BaseModel
from typing import Text, List, Optional

class PaymentMethodSchema(BaseModel):
    id: int
    name: str
    processor_id: str
    status: str
    client_secret: Optional[str]
    client_secret_id: Optional[str]
    