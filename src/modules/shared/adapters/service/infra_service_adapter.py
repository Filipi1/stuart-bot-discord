from typing import Optional
from modules.shared.services.logger.logger_service import LoggerService


class InfraServiceAdapter:
    def __init__(self, context: Optional[str] = None):
        self.logger = LoggerService(context)
