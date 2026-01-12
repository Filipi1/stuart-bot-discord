from http import HTTPMethod
from modules.coach.entities.coach_entity import CoachEntity
from modules.shared.adapters.http.http_adapter import HttpAdapter
from modules.shared.adapters.service.infra_service_adapter import InfraServiceAdapter


class CoachService(InfraServiceAdapter):
    def __init__(self, http_service: HttpAdapter):
        self.__http_service = http_service
        super().__init__(CoachService.__name__)

    async def get_coach(self) -> CoachEntity:
        response = await self.__http_service.request(
            "v1/coach",
            HTTPMethod.GET,
        )
        return CoachEntity(**response)
