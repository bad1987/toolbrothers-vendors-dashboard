from pydantic import BaseModel

class PaymentMethodSchema(BaseModel):
    id: int
    name: str
    processor_id: str
    status: str
    processor_params: str
    