from sqlalchemy import Float, Text, TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from Database.CscartConnexion import CscartBase


class CscartCompanies(CscartBase):
    __tablename__ = "cscart_companies"

    company_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    company = Column(String(255), nullable=True)
    lang_code = Column(String(255), nullable=True)
    status = Column(String(25), nullable=True)

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
    company_id = Column(Integer, nullable=True)
    processor_id = Column(Integer, nullable=True)
    status = Column(String(25), nullable=True)
    
class Cscart_products(CscartBase):
    __tablename__ = "cscart_products"
    product_id = Column(Integer, primary_key=True, nullable=True)
    product_code = Column(Integer)
    company_id = Column(Integer)
    weight = Column(Integer)
    amount = Column(Float, nullable=True)
    master_product_id = Column(Integer)
    product_type = Column(String(25))
    master_product_status = Column(String(25))
    status = Column(String(25))
    
    cscart_product_prices = relationship("Cscart_product_prices", lazy="joined", back_populates="cscart_products")
    cscart_product_descriptions = relationship("Cscart_product_descriptions", lazy="joined", back_populates="cscart_products")

class Cscart_product_descriptions(CscartBase):
    __tablename__ = "cscart_product_descriptions"
    shortname = Column(Integer, primary_key=True, nullable=True)
    full_description = Column(Text, nullable=True)
    short_description = Column(Text, nullable=True)
    product = Column(String(100), nullable=True)
    lang_code = Column(String(100), nullable=True)
    product_id = Column(Integer, ForeignKey("cscart_products.product_id"))
    
    cscart_products = relationship("Cscart_products",  back_populates="cscart_product_descriptions")
    
class Cscart_product_prices(CscartBase):
    __tablename__ = "cscart_product_prices"
    usergroup_id = Column(Integer, primary_key=True, nullable=True)
    price = Column(Float, nullable=True)
    product_id = Column(Integer, ForeignKey("cscart_products.product_id"))
    
    cscart_products = relationship("Cscart_products",  back_populates="cscart_product_prices")
   

class CscartUsers(CscartBase):
    __tablename__ = "cscart_users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    firstname = Column(String(255), nullable=True)
    lastname = Column(String(255), nullable=True)
    
class Cscart_vendor_communications(CscartBase):
    __tablename__ = "cscart_vendor_communications"
    thread_id = Column(Integer, primary_key=True, nullable=True)
    company_id = Column(Integer, nullable=True)
    object_id = Column(Integer, nullable=True)
    object_type = Column(Integer, nullable=True)
    status = Column(String(25), nullable=True)
    last_message = Column(String(255), nullable=True)
    last_message_user_id = Column(Integer, nullable=True)
    last_message_user_type = Column(String(255), nullable=True)
    communication_type = Column(String(255), nullable=True)
    last_updated = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    user_id = Column(Integer, ForeignKey("cscart_users.user_id", ondelete="CASCADE"), nullable=True)
    
    
class Cscart_vendor_communication_messages(CscartBase):
    __tablename__ = "cscart_vendor_communication_messages"
    message_id = Column(Integer, primary_key=True, nullable=True)
    thread_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("cscart_users.user_id", ondelete="CASCADE"), nullable=True)
    user_type = Column(String(25), nullable=True)
    timestamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    message = Column(Text, nullable=True)
    
    cscart_users = relationship("Cscart_vendor_communication_messages", secondary='cscart_users') 