# --------------------------------------------------------------------------
# Setup FastAPI
# --------------------------------------------------------------------------
class Settings:
    SECRET_KEY: str = "secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 10  # in mins 58000
    COOKIE_NAME = "access_token"