from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MemeEntity(BaseModel):
    id: int = Field(alias="id")
    title: str = Field(alias="title")
    description: Optional[str] = Field(default=None)
    image: str = Field(alias="image")
    earned_times: int = Field(default=0)
    updated_at: Optional[datetime] = Field(default=None)

    def last_updated_at(self) -> str:
        return (
            self.updated_at.strftime("%d/%m/%Y %H:%M:%S")
            if self.updated_at
            else "Nunca"
        )
