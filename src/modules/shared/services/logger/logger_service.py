import sys
from typing import Literal

from loguru import logger


class LoggerService:
    def __init__(self, context: str):
        logger.remove()
        logger.level("INFO", color="<white><bg #0066cc>")  # azul
        logger.level("WARNING", color="<white><bg #ffcc00>")  # amarelo
        logger.level("ERROR", color="<white><bg #cc0000>")  # vermelho
        logger.level("DEBUG", color="<white><bg #888888>")  # cinza

        logger.add(
            sys.stdout,
            colorize=True,
            format="     <level> {level:>4} </level> - {message} <dim>({file}:{line})</dim>",
        )
        self.logger = logger.bind(context=context)
        self.logger = self.logger.opt(depth=1, colors=True)

    def debug(self, message):
        self.logger.bind().debug(message)

    def info(self, message):
        self.logger.bind().info(message)

    def warning(self, message):
        self.logger.bind().warning(message)

    def error(self, message):
        self.logger.bind().error(message)

    def title_box(self, message):
        self.logger.bind().info(f"╔{'═' * (len(message) + 2)}╗")
        self.logger.bind().info(f"║ {message} ║")
        self.logger.bind().info(f"╚{'═' * (len(message) + 2)}╝")

    def title_box_warning(self, message):
        self.logger.bind().warning(f"╔{'═' * (len(message) + 2)}╗")
        self.logger.bind().warning(f"║ {message} ║")
        self.logger.bind().warning(f"╚{'═' * (len(message) + 2)}╝")

    def title_box_error(self, message):
        self.logger.bind().error(f"╔{'═' * (len(message) + 2)}╗")
        self.logger.bind().error(f"║ {message} ║")
        self.logger.bind().error(f"╚{'═' * (len(message) + 2)}╝")

    # exibe um dict como tabela
    def dict_to_table(self, message: dict):
        self.logger.bind().info(f"╔{'═' * (len(message) + 30)}╗")
        for key, value in message.items():
            self.logger.bind().info(f"║ {key}: {value}")
        self.logger.bind().info(f"╚{'═' * (len(message) + 30)}╝")

    def result(self, key: str, value: str, level: Literal["info", "warning", "error"]):
        match level:
            case "info":
                self.logger.bind().opt(colors=True, depth=1).info(
                    f"{key} ----------------------------------- <green>{value}</green>"
                )
            case "warning":
                self.logger.bind().opt(colors=True, depth=1).warning(
                    f"{key} ----------------------------------- <yellow>{value}</yellow>"
                )
            case "error":
                self.logger.bind().opt(colors=True, depth=1).error(
                    f"{key} ----------------------------------- <red>{value}</red>"
                )
