import os
import importlib
from typing import List, Dict
from modules.shared.adapters import BotCommand


class CommandDiscoveryService:

    def __init__(self, modules_path: str = "src/modules"):
        self.modules_path = modules_path
        self.discovered_commands: Dict[str, BotCommand] = {}

    def discover_commands(self) -> Dict[str, BotCommand]:
        print("Iniciando descoberta de comandos...")

        self.discovered_commands.clear()

        for root, dirs, files in os.walk(self.modules_path):
            dirs[:] = [d for d in dirs if d != "__pycache__"]

            for file in files:
                if file.endswith("_command.py"):
                    self._process_command_file(root, file)

        return self.discovered_commands

    def _process_command_file(self, root: str, file: str) -> None:
        try:
            rel_path = os.path.relpath(os.path.join(root, file), "src")
            module_path = rel_path.replace(os.sep, ".").replace(".py", "")

            module = importlib.import_module(module_path)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)

                if (
                    isinstance(attr, type)
                    and issubclass(attr, BotCommand)
                    and attr != BotCommand
                ):

                    command_instance = attr()

                    self.discovered_commands[command_instance.name] = command_instance

        except Exception as e:
            print(f"Erro ao processar arquivo {file}: {e}")
            raise e

    def get_command(self, name: str) -> BotCommand:
        return self.discovered_commands.get(name)

    def list_command_names(self) -> List[str]:
        return list(self.discovered_commands.keys())
