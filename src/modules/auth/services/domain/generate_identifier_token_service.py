from modules.auth.services.infra.auth_service import AuthService

from modules.shared.adapters import DomainService

class GenerateIdentifierTokenDomainService(DomainService):
    def __init__(self, auth_service: AuthService):
        self.__auth_service = auth_service
        super().__init__(GenerateIdentifierTokenDomainService.__name__)

    async def process(self, identifier: str) -> str:
        return await self.__auth_service.get_identifier_token(identifier)