from http import HTTPMethod
from modules.shared.adapters.http.http_adapter import HttpAdapter
from modules.shared.adapters import InfraServiceAdapter


class AuthService(InfraServiceAdapter):
    def __init__(self, http_service: HttpAdapter):
        self.__http_service = http_service
        super().__init__(AuthService.__name__)

    async def get_identifier_token(self, identifier: str) -> str:
        response = await self.__http_service.request(
            "v1/auth",
            HTTPMethod.POST,
            body={
                "identifier": identifier,
            },
        )
        return response["token"]
