from sqlalchemy.ext.asyncio import create_async_engine
from pydantic_settings import BaseSettings, SettingsConfigDict


################### START UPs ###################

class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int = 5432
    #AUTH SETTINGS
    SECRET_KEY: str = "your-default-secret-key-for-jwt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def SQLMODEL_DATABASE_URL(self) -> str:
        return (f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")





settings = Settings()

#1st Get your URL
# SQLMODEL_DATABASE_URL = (f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

# STEP 2 BUILD MY ENGINE: responsible for sql alchemy to connect to the database
engine = create_async_engine(settings.SQLMODEL_DATABASE_URL)

