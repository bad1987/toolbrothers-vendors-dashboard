from pydantic import BaseModel
from typing import Text, List, Optional
from App.Http.Schema.ProductDescriptionSchema import ProductDescriptionSchema
from App.Http.Schema.ProductPriceSchema import ProductPriceSchema

class ProductSchema(BaseModel):
    product_id: Optional[int]
    product_code: Optional[str]
    product: Optional[str]
    product_type: Optional[str]
    status: Optional[str]
    weight: Optional[int]
    amount: Optional[int]
    cscart_product_descriptions: Optional[ProductDescriptionSchema] = {}
    cscart_product_prices: Optional[ProductPriceSchema] = {}
    
    def setPrices(self, price):
        self.cscart_product_prices = price
    
    def setProductName(self, name):
        self.product = name
    
    class Config:
        orm_mode = True

    
    