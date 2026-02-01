from modules.shared.adapters.http.http_adapter import HttpAdapter
from modules.shared.adapters.service.infra_service_adapter import InfraServiceAdapter


class ImageService(InfraServiceAdapter):
    def __init__(self, http_service: HttpAdapter):
        self.__http_service = http_service
        super().__init__(ImageService.__name__)

    async def download_image(self, url: str) -> bytes:
        return await self.__http_service.request_image_bytes(url)
