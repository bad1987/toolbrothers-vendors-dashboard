import pathlib

from starlette.config import Config

ROOT = pathlib.Path(__file__).resolve()
BASE_DIR = ROOT.parent

config = Config(BASE_DIR / ".env")


# SMTP CONNEXION
SERVER_HOST = config("SERVER_HOST", str)
SMTP_SENDER_MAIL = config("SMTP_SENDER_MAIL", str)
SMTP_PASSWORD = config("SMTP_PASSWORD", str)
SMTP_SERVER = config("SMTP_SERVER", str)
SMTP_PORT = config("SMTP_PORT", str)

# CONNECTION LOCAL DATABASE
MARIADB_HOST = config("MARIADB_HOST", str)
MARIADB_PORT = config("MARIADB_PORT", int)
MARIADB_USER = config("MARIADB_USER", str)
MARIADB_PASSWORD = config("MARIADB_PASSWORD", str)
MARIADB_DB = config("MARIADB_DB", str)

# CONNECTION CS-CART DATABASE
CSCART_MARIADB_HOST = config("CSCART_MARIADB_HOST", str)
CSCART_MARIADB_PORT = config("CSCART_MARIADB_PORT", int)
CSCART_MARIADB_USER = config("CSCART_MARIADB_USER", str)
CSCART_MARIADB_PASSWORD = config("CSCART_MARIADB_PASSWORD", str)
CSCART_MARIADB_DB = config("CSCART_MARIADB_DB", str)