from datetime import datetime
from typing import List

from fastapi import Depends, Request
from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel
from App.input_ports.schemas.ProductSchema import ProductListResponseSchema, ProductSchema

from App.output_ports.repositories.order_repository import OrderRepository

from sqlalchemy.orm import Session

from App.output_ports.repositories.product_repository import ProductRepository

class ProductUseCase():
    def __init__(self, db_local: Session, db_cscart: Session) -> None:
        self.db_local = db_local
        self.db_cscart = db_cscart
        self.product_repository = ProductRepository(db_local=db_local, db_cscart=db_cscart)

    def get_product_list(self, request: Request, statuses: list, skip: int, limit: int) -> ProductListResponseSchema:
        return self.product_repository.get_products(request, self.db_local, self.db_cscart, statuses, skip, limit)

    def get_product(self, request: Request, product_id: int) -> ProductSchema:
        return self.product_repository.get_product(product_id, request, self.db_local, self.db_cscart)