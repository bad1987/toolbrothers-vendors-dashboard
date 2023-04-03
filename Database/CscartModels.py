from sqlalchemy import Float, Text, TIMESTAMP, Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from Database.CscartConnexion import CscartBase


class CscartCompanies(CscartBase):
    __tablename__ = "cscart_companies"

    company_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    company = Column(String(255), nullable=False)
    status = Column(String(25), nullable=False)
    
class CscartOrders(CscartBase):
    __tablename__ = "cscart_orders"

    order_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    status = Column(String(255), unique=True, index=True, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=True)
    status = Column(String(25), nullable=True)
    firstname = Column(String(25), nullable=True)
    lastname = Column(String(25), nullable=True)
    email = Column(String(25), nullable=True)
    phone = Column(String(25), nullable=True)
    company = Column(String(255), nullable=True)
    total = Column(Float, nullable=True)
    
class Cscart_payments(CscartBase):
    __tablename__ = "cscart_payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    processor_params = Column(Text, nullable=True)
    company_id = Column(Integer, nullable=False)
    processor_id = Column(Integer, nullable=False)
    status = Column(String(25), nullable=False)
    
class Cscart_products(CscartBase):
    __tablename__ = "cscart_products"
    product_id = Column(Integer, primary_key=True, nullable=False)
    product_code = Column(Integer)
    company_id = Column(Integer)
    weight = Column(Integer)
    amount = Column(Float, nullable=True)
    master_product_id = Column(Integer)
    product_type = Column(String(25))
    master_product_status = Column(String(25))
    status = Column(String(25))
    
    cscart_product_prices = relationship("Cscart_product_prices",  back_populates="cscart_products")
    cscart_product_descriptions = relationship("Cscart_product_descriptions",  back_populates="cscart_products")

class Cscart_product_descriptions(CscartBase):
    __tablename__ = "cscart_product_descriptions"
    lang_code = Column(Integer, primary_key=True, nullable=False)
    full_description = Column(Text, nullable=True)
    short_description = Column(Text, nullable=True)
    product_id = Column(Integer, ForeignKey("cscart_products.product_id"))
    
    cscart_products = relationship("Cscart_products",  back_populates="cscart_product_descriptions")
    
class Cscart_product_prices(CscartBase):
    __tablename__ = "cscart_product_prices"
    usergroup_id = Column(Integer, primary_key=True, nullable=False)
    price = Column(Float, nullable=True)
    product_id = Column(Integer, ForeignKey("cscart_products.product_id"))
    
    cscart_products = relationship("Cscart_products",  back_populates="cscart_product_prices")