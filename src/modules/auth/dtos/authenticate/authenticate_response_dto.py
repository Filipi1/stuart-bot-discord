from pydantic import BaseModel
from pydantic import Field


class AuthenticateResponseDto(BaseModel):
    token: str = Field(alias="token")
