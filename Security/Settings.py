# --------------------------------------------------------------------------
# Setup FastAPI
# --------------------------------------------------------------------------
class Settings:
    SECRET_KEY: str = "secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 58000  # in mins
    COOKIE_NAME = "access_token"