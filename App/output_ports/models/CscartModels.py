from sqlalchemy import Float, Text, TIMESTAMP, Column, ForeignKey, Integer, String, text, Boolean
from sqlalchemy.orm import relationship

from App.output_ports.db.CscartConnexion import CscartBase

class CscartCompanies(CscartBase):
    __tablename__ = "cscart_companies"

    company_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    company = Column(String(255), nullable=True)
    lang_code = Column(String(255), nullable=True)
    status = Column(String(25), nullable=True)
 
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
    amount = Column(Integer, nullable=True)
    master_product_id = Column(Integer)
    product_type = Column(String(25))
    master_product_status = Column(String(25))
    timestamp = Column(Integer)
    status = Column(String(25))
    manual_change = Column(Boolean)

    # cscart_order_details = relationship("Cscart_products",  back_populates="cscart_order_details", cascade="all, delete") 
    price = relationship("Cscart_product_prices", back_populates="product", uselist=False)
    description = relationship("Cscart_product_descriptions", back_populates="linkedProduct")

class Cscart_product_descriptions(CscartBase):
    __tablename__ = "cscart_product_descriptions"
    shortname = Column(String(100), nullable=False)
    full_description = Column(Text, nullable=True)
    short_description = Column(Text, nullable=True)
    product = Column(String(100), nullable=True)
    lang_code = Column(String(100), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("cscart_products.product_id"), primary_key=True, index=True)
    
    linkedProduct = relationship("Cscart_products",  back_populates="description")
    
class Cscart_product_prices(CscartBase):
    __tablename__ = "cscart_product_prices"
    usergroup_id = Column(Integer, primary_key=True, nullable=True)
    price = Column(Float, nullable=True)
    product_id = Column(Integer, ForeignKey("cscart_products.product_id"), primary_key=True)
    
    product = relationship("Cscart_products",  back_populates="price")
   
class Cscart_vendor_communications(CscartBase):
    __tablename__ = "cscart_vendor_communications"
    thread_id = Column(Integer, primary_key=True, nullable=True)
    company_id = Column(Integer, nullable=True)
    storefront_id = Column(Integer, nullable=True)
    object_id = Column(Integer, nullable=True)
    object_type = Column(Integer, nullable=True)
    status = Column(String(25), nullable=True)
    last_message = Column(Text, nullable=True)
    last_message_user_id = Column(Integer, nullable=True)
    last_message_user_type = Column(String(255), nullable=True)
    communication_type = Column(String(255), nullable=True)
    last_updated = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    user_id = Column(Integer, ForeignKey("cscart_users.user_id", ondelete="CASCADE"), nullable=True)
    
    
class CscartUsers(CscartBase):
    __tablename__ = "cscart_users"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    firstname = Column(String(255), nullable=True)
    lastname = Column(String(255), nullable=True)
    company_id = Column(String(255), nullable=False)
    
class Cscart_vendor_communication_messages(CscartBase):
    __tablename__ = "cscart_vendor_communication_messages"
    message_id = Column(Integer, primary_key=True, nullable=True)
    thread_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("cscart_users.user_id", ondelete="CASCADE"), nullable=True)
    user_type = Column(String(25), nullable=True)
    timestamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    message = Column(Text, nullable=True)
    
    cscart_users = relationship("Cscart_vendor_communication_messages", secondary='cscart_users')   
    

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
    user_id = Column(Integer, ForeignKey("cscart_users.user_id", ondelete="CASCADE"), nullable=True)
    total = Column(Float, nullable=True)
    subtotal = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    timestamp = Column(Integer, nullable=True)
    b_address = Column(String(255), nullable=True)
    b_address_2 = Column(String(255), nullable=True)
    b_city = Column(String(255), nullable=True)
    b_state = Column(String(255), nullable=True)
    b_zipcode = Column(Integer, nullable=True)
    shipping_cost = Column(Float, nullable=True)
   
class CscartOrderDetails(CscartBase):
    __tablename__ = "cscart_order_details"
    item_id = Column(Integer, primary_key=True, nullable=True)
    order_id = Column(Integer, ForeignKey("cscart_orders.order_id", ondelete="CASCADE"), nullable=True)
    product_id = Column(Integer, ForeignKey("cscart_products.product_id", ondelete="CASCADE"), nullable=True)
    product_code = Column(String(255), nullable=True)
    price = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)
    extra = Column(String(255), nullable=False)
    
    cscart_orders = relationship("CscartOrderDetails", secondary='cscart_orders') 
    cscart_products = relationship("CscartOrderDetails", secondary='cscart_products') 
  