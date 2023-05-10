from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import CscartSettingConnexion

DATABASE_URL = f"mariadb+mariadbconnector://{CscartSettingConnexion.MARIADB_USER}:{CscartSettingConnexion.MARIADB_PASSWORD}@{CscartSettingConnexion.MARIADB_HOST}:{CscartSettingConnexion.MARIADB_PORT}/{CscartSettingConnexion.MARIADB_DB}"

engine = create_engine(
    DATABASE_URL
)
CscartSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

CscartBase = declarative_base()