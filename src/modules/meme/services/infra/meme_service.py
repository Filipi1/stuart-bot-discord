from http import HTTPMethod
from modules.meme.entities import MemeEntity
from modules.shared.adapters.http.http_adapter import HttpAdapter
from modules.shared.adapters.service.infra_service_adapter import InfraServiceAdapter


class MemeService(InfraServiceAdapter):
    def __init__(self, http_service: HttpAdapter):
        self.__http_service = http_service
        super().__init__(MemeService.__name__)

    async def get_meme(self) -> MemeEntity:
        response = await self.__http_service.request(
            "v1/meme",
            HTTPMethod.GET,
        )
        return MemeEntity(**response)