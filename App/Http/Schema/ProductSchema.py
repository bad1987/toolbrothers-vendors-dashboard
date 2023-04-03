from pydantic import BaseModel
from typing import Text, List, Optional
from App.Http.Schema.ProductDescriptionSchema import ProductDescriptionSchema
from App.Http.Schema.ProductPriceSchema import ProductPriceSchema

class ProductSchema(BaseModel):
    product_id: Optional[int]
    product_code: Optional[str]
    product_type: Optional[str]
    status: Optional[str]
    cscart_product_descriptions: Optional[ProductDescriptionSchema] = {}
    cscart_product_prices: Optional[ProductPriceSchema] = {}
    
    class Config:
        orm_mode = True

    
    