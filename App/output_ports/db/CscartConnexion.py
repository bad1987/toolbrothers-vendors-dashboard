from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import CscartSettingConnexion

DATABASE_URL = f"mariadb+mariadbconnector://{CscartSettingConnexion.CSCART_MARIADB_USER}:{CscartSettingConnexion.CSCART_MARIADB_PASSWORD}@{CscartSettingConnexion.CSCART_MARIADB_HOST}:{CscartSettingConnexion.CSCART_MARIADB_PORT}/{CscartSettingConnexion.CSCART_MARIADB_DB}"

engine = create_engine(
    DATABASE_URL
)
CscartSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

CscartBase = declarative_base()