from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text, BigInteger, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.types import Text
from Database.Connexion import Base
from App.Enums.UserRoleEnum import UserRoleEnum
from App.Enums.UserEnums import UserStatusEnum
from App.Enums.LanguageEnum import LanguageEnum


class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=False, index=True, nullable=False)
    company_id = Column(Integer, unique=True, index=True, nullable=True)
    password = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=True)
    lastname = Column(String(255), nullable=True)
    default_language = Column(Enum(LanguageEnum, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    roles = Column(Enum(UserRoleEnum, values_callable=lambda obj: [e.value for e in obj]), nullable = False)
    status = Column(Enum(UserStatusEnum, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    api_token = Column(String(255), nullable=True, unique=True)
    parent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    permissions = relationship("Permission", secondary='user_permissions')
    
    
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
    client_secret = Column(String(255), nullable=True)
    client_secret_id = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_method.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    
    # users = relationship("User", back_populates="payment_method")
    # payment_method = relationship("Payment_method_vendor", back_populates="payment_method")
    
class Platform_settings(Base):
    __tablename__ = "platform_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    platform_id = Column(BigInteger, nullable=True)
    referrer_id = Column(BigInteger, nullable=True)
    api_id = Column(BigInteger, nullable=True)
    api_secret = Column(BigInteger, nullable=True)
    access_token = Column(BigInteger, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    platform_url = Column(String(250), nullable=True)
    method_payment_id = Column(BigInteger, nullable=True)
    shipping_profile_id = Column(BigInteger, nullable=True)
    export_product_link = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    
    # payment_method_vendor = relationship("Payment_method_vendor",  back_populates="payment_method", cascade="all, delete")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(25), nullable=False, unique=True) 
    mode = Column(String(25), nullable=False)
    model_name = Column(String(25), nullable=False)
    description = Column(Text, nullable=True)

class User_Permission(Base):
    __tablename__ = "user_permissions"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

class Login_Attempt(Base):
    __tablename__ = "login_attempts"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ip = Column(String(20), unique=True, nullable=False)
    count = Column(Integer, default=0)
    timestamp = Column(Integer, nullable=True)
