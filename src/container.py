from modules.auth.services.domain.generate_identifier_token_service import (
    GenerateIdentifierTokenDomainService,
)
from modules.auth.services.infra.auth_service import AuthService
from modules.coach.services.application.get_coach_service import (
    GetCoachApplicationService,
)
from modules.coach.services.domain.fetch_coach_service import FetchCoachDomainService
from modules.coach.services.infra.coach_service import CoachService
from modules.meme.services.application.create_meme_service import (
    CreateMemeApplicationService,
)
from modules.meme.services.application.get_meme_service import GetMemeApplicationService
from modules.meme.services.application.get_memes_count import (
    GetMemesCountApplicationService,
)
from modules.meme.services.application.get_memes_status import (
    GetMemesStatusApplicationService,
)
from modules.meme.services.domain.create_meme_service import CreateMemeDomainService
from modules.meme.services.domain.fetch_meme_service import FetchMemeDomainService
from modules.meme.services.domain.fetch_memes_status_service import (
    FetchMemesStatusDomainService,
)
from modules.meme.services.infra.meme_service import MemeService
from modules.shared.services.image.image_service import ImageService
from modules.shared.services.requests import RequestsService
from modules.shared.settings.settings import Settings


class Containers:
    def __init__(self):
        # Domain
        self.__settings = Settings()
        self.__http_service = RequestsService(
            base_url=self.__settings.STUART_API_BASE_URL
        )
        self.__auth_service = AuthService(http_service=self.__http_service)
        self.__meme_service = MemeService(http_service=self.__http_service)
        self.__coach_service = CoachService(http_service=self.__http_service)
        self.__generate_identifier_token_service = GenerateIdentifierTokenDomainService(
            auth_service=self.__auth_service
        )
        self.__fetch_meme = FetchMemeDomainService(
            meme_service=self.__meme_service,
            generate_identifier_token_service=self.__generate_identifier_token_service,
        )
        self.__fetch_memes_status = FetchMemesStatusDomainService(
            meme_service=self.__meme_service
        )
        self.__fetch_coach = FetchCoachDomainService(coach_service=self.__coach_service)
        self.__create_meme_domain = CreateMemeDomainService(
            meme_service=self.__meme_service
        )
        self.__image_service = ImageService(http_service=self.__http_service)

        # Application
        self.get_meme = GetMemeApplicationService(fetch_meme_service=self.__fetch_meme)
        self.get_memes_status = GetMemesStatusApplicationService(
            fetch_memes_status_service=self.__fetch_memes_status
        )
        self.get_memes_count = GetMemesCountApplicationService(
            fetch_memes_status_service=self.__fetch_memes_status
        )
        self.get_coach = GetCoachApplicationService(
            fetch_coach_service=self.__fetch_coach
        )
        self.create_meme = CreateMemeApplicationService(
            create_meme_domain_service=self.__create_meme_domain,
            image_service=self.__image_service,
            get_memes_count=self.get_memes_count,
        )


container = Containers()
