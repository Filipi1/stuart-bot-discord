from modules.meme.entities.meme_entity import MemeEntity
from modules.meme.services.infra.meme_service import MemeService
from modules.shared.adapters import DomainService


class FetchMemeDomainService(DomainService):
    def __init__(
        self,
        meme_service: MemeService,
    ):
        self.__meme_service = meme_service
        super().__init__(FetchMemeDomainService.__name__)

    async def process(self) -> MemeEntity:
        return await self.__meme_service.get_meme()
