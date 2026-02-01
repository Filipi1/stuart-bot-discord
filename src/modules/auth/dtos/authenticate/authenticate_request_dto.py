from pydantic import BaseModel
from pydantic import Field


class AuthenticateRequestDto(BaseModel):
    identifier: str = Field(description="Identificador do usuário")
