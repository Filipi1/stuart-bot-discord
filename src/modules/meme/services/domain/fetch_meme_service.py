from modules.auth.services.domain.generate_identifier_token_service import GenerateIdentifierTokenDomainService
from modules.meme.entities.meme_entity import MemeEntity
from modules.meme.services.infra.meme_service import MemeService
from modules.shared.adapters import DomainService


class FetchMemeDomainService(DomainService):
    def __init__(
        self,
        meme_service: MemeService,
        generate_identifier_token_service: GenerateIdentifierTokenDomainService,
    ):
        self.__generate_identifier_token_service = generate_identifier_token_service
        self.__meme_service = meme_service
        super().__init__(FetchMemeDomainService.__name__)

    async def process(self, username: str) -> MemeEntity:
        request_token = await self.__generate_identifier_token_service.process(username)
        return await self.__meme_service.get_meme(request_token)
