import pathlib

from starlette.config import Config

ROOT = pathlib.Path(__file__).resolve()
BASE_DIR = ROOT.parent

config = Config(BASE_DIR / ".env")


# SMTP CONNEXION
SMTP_SERVER_HOST = config("SERVER_HOST", str)
SMTP_SENDER_MAIL = config("SMTP_SENDER_MAIL", str)
SMTP_PASSWORD = config("SMTP_PASSWORD", str)
SMTP_SERVER = config("SMTP_SERVER", str)
SMTP_PORT = config("SMTP_PORT", str)