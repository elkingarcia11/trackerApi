from pydantic import BaseSettings

class Settings(BaseSettings):
    OAUTH2_SECRET_KEY : str
    OAUTH2_ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : str

settings = Settings()