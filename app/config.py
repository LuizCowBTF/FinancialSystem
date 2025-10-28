from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    APP_NAME: str = 'AlmeidaSystem'
    ENV: str = 'dev'
    SECRET_KEY: str = 'change_me_please'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 3306
    DB_USER: str = 'root'
    DB_PASSWORD: str = ''
    DB_NAME: str = 'almeida_db'

    CORS_ORIGINS: str = ''
    REDIS_URL: str = 'redis://localhost:6379/0'

    def cors_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(',') if o.strip()]

settings = Settings()
