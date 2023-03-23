from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.types import Text
from Database.Connexion import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=False, index=True, nullable=False)
    company_id = Column(Integer, unique=True, index=True, nullable=True)
    password = Column(String(255), nullable=False)
    roles = Column(String(255), nullable = False)
    status = Column(String(25), nullable=False)
    
    # payment_method_vendor = relationship("Payment_method_vendor",  back_populates="users", cascade="all, delete")
    
class Payment_method(Base):
    __tablename__ = "payment_method"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    processor_id = Column(Integer, nullable=False)
    
    # payment_method_vendor = relationship("Payment_method_vendor",  back_populates="payment_method", cascade="all, delete")
    
class Payment_method_vendor(Base):
    __tablename__ = "payment_method_vendor"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    processor_id = Column(Integer, nullable=True)
    payment_id = Column(Integer, nullable=False)
    status = Column(String(25), nullable=False)
    processor_params = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_method.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)

    # users = relationship("User", back_populates="payment_method")
    # payment_method = relationship("Payment_method_vendor", back_populates="payment_method")
    
class Platform_settings(Base):
    __tablename__ = "platform_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    platform_id = Column(String(100), index=True, nullable=True)
    referrer_id = Column(String(100), index=True, nullable=True)
    api_id = Column(String(100), index=True, nullable=True)
    api_secret = Column(String(100), index=True, nullable=True)
    access_token = Column(String(100), index=True, nullable=True)
    platform_url = Column(String(250), index=True, nullable=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    processor_id = Column(Integer, nullable=False)
    
    # payment_method_vendor = relationship("Payment_method_vendor",  back_populates="payment_method", cascade="all, delete")
    # Plenty ID:
    # Referrer ID:
    # API ID:
    # API SECRET:
    # ACCESS TOKEN:
    # Plenty Url:
    # Method of payment ID:
    # Shipping profile ID: VAT:
    
    