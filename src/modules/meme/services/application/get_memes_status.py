import discord
from modules.meme.dtos.fetch_current_memes_count.fetch_memes_status_response_dto import (
    FetchMemesStatusResponseDto,
)
from modules.meme.services.domain.fetch_memes_status_service import (
    FetchMemesStatusDomainService,
)
from modules.shared.adapters import DomainService


class GetMemesStatusApplicationService(DomainService):
    def __init__(
        self,
        fetch_memes_status_service: FetchMemesStatusDomainService,
    ):
        self.__fetch_memes_status_service = fetch_memes_status_service
        super().__init__(GetMemesStatusApplicationService.__name__)

    async def process(self) -> discord.Embed:
        response: FetchMemesStatusResponseDto = (
            await self.__fetch_memes_status_service.process()
        )
        self.logger.dict_to_table(response.model_dump())
        embed = discord.Embed(title="🎲 Status dos memes", color=0xFF6B6B)
        embed.add_field(name="Total de memes", value=response.total_memes)
        embed.add_field(
            name="Meme mais antigo que ainda não foi sorteado",
            value=response.oldest_unsorted_meme_date,
        )
        embed.add_field(
            name="Quantidade de memes que ainda não foram sorteados",
            value=response.unsorted_memes_count,
        )
        embed.add_field(
            name="Meme mais sorteado", value=response.most_sorted_meme.title
        )
        return embed
