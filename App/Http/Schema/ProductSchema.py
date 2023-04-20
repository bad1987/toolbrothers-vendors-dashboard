from pydantic import BaseModel
from typing import Text, List, Optional
from App.Http.Schema.ProductDescriptionSchema import ProductDescriptionSchema
from App.Http.Schema.ProductPriceSchema import ProductPriceSchema

class ProductSchema(BaseModel):
    product_id: Optional[int]
    product_code: Optional[str]
    price: Optional[float]
    status: Optional[str]
    amount: Optional[int]
    product_type: Optional[str]
    weight: Optional[int]
    product: Optional[str]

class ProductUpdateSchemaIn(BaseModel):
    product_id: int
    status: Optional[str]
    amount: Optional[int]
    price: Optional[float]

    class Config:
        orm_mode = True

class ProductListSchemaOut(BaseModel):
    products: List[ProductSchema]
    total: Optional[int]


    
    