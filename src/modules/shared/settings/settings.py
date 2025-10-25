from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = Field(default="production")
    BOT_TOKEN: str
    STUART_API_BASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
