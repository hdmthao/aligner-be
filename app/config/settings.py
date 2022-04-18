from pydantic import BaseSettings

class DatabaseSettings(BaseSettings):
    URL: str
    NAME: str

    class Config:
        env_prefix = 'DB_'

class Settings(DatabaseSettings):
    pass

settings = Settings() # pyright: ignore
