from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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