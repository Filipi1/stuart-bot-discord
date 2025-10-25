from modules.meme.dtos.fetch_current_memes_count.fetch_memes_status_response_dto import (
    FetchMemesStatusResponseDto,
)
from modules.meme.services.infra.meme_service import MemeService
from modules.shared.adapters import DomainService


class FetchMemesStatusDomainService(DomainService):
    def __init__(
        self,
        meme_service: MemeService,
    ):
        self.__meme_service = meme_service
        super().__init__(FetchMemesStatusDomainService.__name__)

    async def process(self) -> FetchMemesStatusResponseDto:
        return await self.__meme_service.get_memes_status()
