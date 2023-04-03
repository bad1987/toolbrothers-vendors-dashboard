from pydantic import BaseModel
from typing import List, Optional

class PlentyMarketSchema(BaseModel):
    platform_id: Optional[int]
    referrer_id: Optional[int]
    api_id: Optional[int]
    api_secret: Optional[int]
    access_token: Optional[int]
    platform_url: Optional[str]
    method_payment_id: Optional[int]
    shipping_profile_id: Optional[int]
    export_product_link: Optional[str]
    