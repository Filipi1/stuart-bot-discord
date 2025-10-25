from datetime import datetime
from pydantic import BaseModel, Field

from modules.meme.entities import MemeEntity


class EarnedMemeEntity(BaseModel):
    id: int = Field(alias="id")
    user_id: int = Field(alias="userId")
    meme_id: int = Field(alias="memeId")
    earned_times: int = Field(alias="earnedTimes")
    meme: MemeEntity = Field(alias="memes")
    updated_at: datetime = Field(alias="updatedAt")
    created_at: datetime = Field(alias="createdAt")
