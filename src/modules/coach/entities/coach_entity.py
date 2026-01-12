from datetime import datetime
from pydantic import BaseModel, Field


class CoachEntity(BaseModel):
    id: int = Field(alias="id")
    message: str = Field(alias="message")
    author: str = Field(alias="author")
    created_at: datetime = Field(alias="created_at")
    updated_at: datetime = Field(alias="updated_at")

    def format_author(self) -> str:
        """Formata o autor no formato 'Sobrenome, Nome'"""
        parts = self.author.split()
        if len(parts) >= 2:
            sobrenome = parts[-1]
            nomes = " ".join(parts[:-1])
            return f"{sobrenome}, {nomes}"
        return self.author
