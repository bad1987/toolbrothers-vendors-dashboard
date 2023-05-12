from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from fastapi import Request

from App.input_ports.schemas.ProductSchema import ProductListResponseSchema, ProductSchema

class IProductRepository(ABC):

    @abstractmethod
    async def get_products(self,request: Request, db_local: Session, db_cscart: Session, statuses: list, skip: int, limit: int) -> ProductListResponseSchema:
        ...

    @abstractmethod
    async def get_product(self,product_id: int, request: Request, db_local: Session, db_cscart: Session) -> ProductSchema:
        ...