from sqlalchemy import Boolean, Column, TIMESTAMP, Integer, String, Float, Text
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