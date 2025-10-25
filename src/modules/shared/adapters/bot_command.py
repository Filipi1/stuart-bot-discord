from abc import ABC, abstractmethod
from typing import Any, List

from modules.shared.dataclasses import CommandOption


class BotCommand(ABC):
    def __init__(self, name: str, description: str, options: List[CommandOption]):
        self.name = name
        self.description = description
        self.options = options

    @abstractmethod
    async def process(self, **kwargs) -> Any:
        raise NotImplementedError("Comando não implementado")
