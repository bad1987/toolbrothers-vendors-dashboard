import pathlib

from starlette.config import Config

ROOT = pathlib.Path(__file__).resolve()
BASE_DIR = ROOT.parent

config = Config(BASE_DIR / ".env.cscart")

CSCART_MARIADB_HOST = config("CSCART_MARIADB_HOST", str)
CSCART_MARIADB_PORT = config("CSCART_MARIADB_PORT", int)
CSCART_MARIADB_USER = config("CSCART_MARIADB_USER", str)
CSCART_MARIADB_PASSWORD = config("CSCART_MARIADB_PASSWORD", str)
CSCART_MARIADB_DB = config("CSCART_MARIADB_DB", str)
