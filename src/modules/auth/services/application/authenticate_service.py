from modules.auth.services.domain.generate_identifier_token_service import (
    GenerateIdentifierTokenDomainService,
)
from src.modules.auth.dtos.authenticate import (
    AuthenticateRequestDto,
    AuthenticateResponseDto,
)

from src.modules.shared.adapters import ApplicationService


class AuthenticateApplicationService(ApplicationService):
    def __init__(
        self, generate_identifier_token_service: GenerateIdentifierTokenDomainService
    ):
        self.__generate_identifier_token_service = generate_identifier_token_service
        super().__init__(AuthenticateApplicationService.__name__)

    async def process(self, input: AuthenticateRequestDto) -> AuthenticateResponseDto:
        token = await self.__generate_identifier_token_service.process(input.identifier)
        return AuthenticateResponseDto(token=token)
