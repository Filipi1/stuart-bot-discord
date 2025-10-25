from modules.meme.dtos.fetch_current_memes_count.fetch_memes_status_response_dto import (
    FetchMemesStatusResponseDto,
)
from modules.meme.services.domain.fetch_memes_status_service import (
    FetchMemesStatusDomainService,
)
from modules.shared.adapters import DomainService


class GetMemesCountApplicationService(DomainService):
    def __init__(
        self,
        fetch_memes_status_service: FetchMemesStatusDomainService,
    ):
        self.__fetch_memes_status_service = fetch_memes_status_service
        super().__init__(GetMemesCountApplicationService.__name__)

    async def process(self) -> int:
        response: FetchMemesStatusResponseDto = (
            await self.__fetch_memes_status_service.process()
        )
        return response.total_memes
