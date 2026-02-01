from typing import Optional

from modules.meme.services.infra.meme_service import MemeService
from modules.shared.adapters import DomainService


class CreateMemeDomainService(DomainService):
    def __init__(self, meme_service: MemeService):
        self.__meme_service = meme_service
        super().__init__(CreateMemeDomainService.__name__)

    async def process(
        self,
        title: str,
        description: Optional[str],
        image_bytes: bytes,
        image_filename: str,
        content_type: str,
    ) -> dict:
        return await self.__meme_service.create_meme(
            title=title,
            description=description,
            image_bytes=image_bytes,
            image_filename=image_filename,
            content_type=content_type,
        )
