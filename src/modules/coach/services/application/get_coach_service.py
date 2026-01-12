import discord
from modules.coach.entities.coach_entity import CoachEntity
from modules.shared.adapters import DomainService
from modules.coach.services.domain.fetch_coach_service import FetchCoachDomainService


class GetCoachApplicationService(DomainService):
    def __init__(
        self,
        fetch_coach_service: FetchCoachDomainService,
    ):
        self.__fetch_coach_service = fetch_coach_service
        super().__init__(GetCoachApplicationService.__name__)

    async def process(self) -> discord.Embed:
        entity: CoachEntity = await self.__fetch_coach_service.process()
        self.logger.dict_to_table(entity.model_dump())

        formatted_author = entity.format_author()
        title = f'*"{entity.message}"*'
        description = f'-- {formatted_author}'

        embed = discord.Embed(
            title=title,
            description=description,
            color=0xFF6B6B,
        )

        return embed
