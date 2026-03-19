import io
import discord
from modules.meme.entities.meme_entity import MemeEntity
from modules.meme.services.domain.fetch_meme_service import FetchMemeDomainService
from modules.shared.adapters import DomainService
from modules.shared.services.image.image_service import ImageService


def _filename_from_url(url: str) -> str:
    name = url.rstrip("/").split("/")[-1]
    return name if name and "." in name else "meme.jpg"


class GetMemeApplicationService(DomainService):
    def __init__(
        self,
        fetch_meme_service: FetchMemeDomainService,
        image_service: ImageService,
    ):
        self.__fetch_meme_service = fetch_meme_service
        self.__image_service = image_service
        super().__init__(GetMemeApplicationService.__name__)

    async def process(self, username: str) -> tuple[discord.Embed, discord.File]:
        entity: MemeEntity = await self.__fetch_meme_service.process(username)
        self.logger.dict_to_table(entity.model_dump())

        image_bytes = await self.__image_service.download_image(entity.image)
        filename = _filename_from_url(entity.image)
        file = discord.File(fp=io.BytesIO(image_bytes), filename=filename)

        embed = discord.Embed(
            title=f"Tu é {entity.title}",
            description=entity.description,
            color=0xFF6B6B,
        )
        embed.set_image(url=f"attachment://{filename}")
        embed.set_footer(
            text=f"🧘 {entity.earned_times} vezes que a galera personificou isso"
        )
        return embed, file
