from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import Setting

DATABASE_URL = f"mariadb+mariadbconnector://{Setting.CSCART_MARIADB_USER}:{Setting.CSCART_MARIADB_PASSWORD}@{Setting.CSCART_MARIADB_HOST}:{Setting.CSCART_MARIADB_PORT}/{Setting.CSCART_MARIADB_DB}"

engine = create_engine(
    DATABASE_URL
)
CscartSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

CscartBase = declarative_base()