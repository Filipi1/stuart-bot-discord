import discord
from typing import Dict
from modules.shared.adapters import BotCommand
from modules.shared.services import CommandDiscoveryService


class CommandRegistrationService:
    
    def __init__(self, client: discord.Client):
        self.client = client
        self.tree = discord.app_commands.CommandTree(client)
        self.discovery_service = CommandDiscoveryService()
        self.registered_commands: Dict[str, BotCommand] = {}
    
    def register_all_commands(self) -> None:
        commands = self.discovery_service.discover_commands()
        
        for name, command in commands.items():
            self._register_command(command)
            self.registered_commands[name] = command
    
    def _register_command(self, command: BotCommand) -> None:
        # Cria callback específico baseado nas opções do comando
        callback = self._create_specific_callback(command)
        
        discord_command = discord.app_commands.Command(
            name=command.name,
            description=command.description,
            callback=callback
        )
        
        self.tree.add_command(discord_command)
    
    def _create_specific_callback(self, command: BotCommand):
        # Se não tem opções, cria callback simples
        if not command.options:
            async def callback(interaction: discord.Interaction):
                try:
                    await command.process(interaction)
                except Exception as e:
                    print(f"Erro ao executar comando {command.name}: {e}")
            return callback
        
        # Se tem opções, cria callback com parâmetros específicos
        option_names = [opt.name for opt in command.options]
        
        if len(option_names) == 1:
            # Comando com 1 parâmetro - cria callback específico
            param_name = option_names[0]
            async def callback(interaction: discord.Interaction, name: str = ""):
                try:
                    await command.process(interaction, name)
                except Exception as e:
                    print(f"Erro ao executar comando {command.name}: {e}")
            return callback
        else:
            # Comando com múltiplos parâmetros - cria callback com todos os parâmetros
            param_names = option_names
            if len(param_names) == 2:
                async def callback(interaction: discord.Interaction, param1: str = "", param2: str = ""):
                    try:
                        params = {param_names[0]: param1, param_names[1]: param2}
                        await command.process(interaction, **params)
                    except Exception as e:
                        print(f"Erro ao executar comando {command.name}: {e}")
                return callback
            else:
                # Para mais de 2 parâmetros, usa abordagem genérica
                async def callback(interaction: discord.Interaction):
                    try:
                        await command.process(interaction)
                    except Exception as e:
                        print(f"Erro ao executar comando {command.name}: {e}")
                return callback
    
    async def sync_commands(self) -> None:
        try:
            synced = await self.tree.sync()
            for command in synced:
                print(f"Comando {command.name} sincronizado")
        except Exception as e:
            print(f"Erro ao sincronizar comandos: {e}")
