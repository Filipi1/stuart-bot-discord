from modules.coach.entities.coach_entity import CoachEntity
from modules.coach.services.infra.coach_service import CoachService
from modules.shared.adapters import DomainService


class FetchCoachDomainService(DomainService):
    def __init__(
        self,
        coach_service: CoachService,
    ):
        self.__coach_service = coach_service
        super().__init__(FetchCoachDomainService.__name__)

    async def process(self) -> CoachEntity:
        return await self.__coach_service.get_coach()
