from modules.meme.services.application.get_meme_service import GetMemeApplicationService
from modules.meme.services.domain.fetch_meme_service import FetchMemeDomainService
from modules.meme.services.infra.meme_service import MemeService
from modules.shared.services.requests import RequestsService
from modules.shared.settings.settings import Settings

class Containers:
    def __init__(self):
        # Domain
        self.__settings = Settings()
        self.__http_service = RequestsService(
            base_url=self.__settings.STUART_API_BASE_URL
        )
        self.__meme_service = MemeService(
            http_service=self.__http_service
        )
        self.__fetch_meme = FetchMemeDomainService(
            meme_service=self.__meme_service
        )

        # Application
        self.get_meme = GetMemeApplicationService(
            fetch_meme_service=self.__fetch_meme
        )
        
container = Containers()