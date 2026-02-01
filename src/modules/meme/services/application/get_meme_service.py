import discord
from modules.meme.entities.meme_entity import MemeEntity
from modules.shared.adapters import DomainService
from modules.meme.services.domain.fetch_meme_service import FetchMemeDomainService


class GetMemeApplicationService(DomainService):
    def __init__(
        self,
        fetch_meme_service: FetchMemeDomainService,
    ):
        self.__fetch_meme_service = fetch_meme_service
        super().__init__(GetMemeApplicationService.__name__)

    async def process(self, username: str) -> discord.Embed:
        entity: MemeEntity = await self.__fetch_meme_service.process(username)
        self.logger.dict_to_table(entity.model_dump())

        embed = discord.Embed(
            title=f"Tu é {entity.title}",
            description=entity.description,
            color=0xFF6B6B,
        )

        embed.set_image(url=entity.image)
        embed.set_footer(
            text=f"🧘 {entity.earned_times} vezes que a galera personificou isso"
        )
        return embed
