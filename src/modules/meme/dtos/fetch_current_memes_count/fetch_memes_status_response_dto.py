from typing import Optional

from pydantic import BaseModel, Field

from modules.meme.entities import MemeEntity


class FetchMemesStatusResponseDto(BaseModel):
    total_memes: int = Field()
    oldest_unsorted_meme_date: Optional[str] = Field(
        description="Data do meme mais antigo que ainda não foi sorteado"
    )
    unsorted_memes_count: int = Field(
        description="Quantidade de memes que ainda não foram sorteados"
    )
    most_sorted_meme: Optional[MemeEntity] = Field(
        description="Meme que foi mais sorteado"
    )
