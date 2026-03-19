from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = Field(default="production")
    BOT_TOKEN: str
    STUART_API_BASE_URL: str
    DISCORD_GUILD_ID: Optional[int] = Field(default=None)
    PORT: int = Field(default=10300, description="Porta do servidor HTTP de health check.")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
