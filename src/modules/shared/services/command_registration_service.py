import discord
from typing import Dict, Optional

from modules.shared.adapters import BotCommand
from modules.shared.services import CommandDiscoveryService
from modules.shared.services.requests.exceptions import HttpException


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
            name=command.name, description=command.description, callback=callback
        )

        self.tree.add_command(discord_command)

    async def _handle_error(
        self, interaction: discord.Interaction, error: Exception, command_name: str
    ) -> None:
        """Trata erros e envia resposta ao Discord"""
        # Não exibir erro ao usuário quando a interação já foi respondida (40060);
        # evita mensagem confusa e possível double-ack.
        if (
            isinstance(error, discord.HTTPException)
            and getattr(error, "code", None) == 40060
        ):
            print(
                f"[{command_name}] Interação já reconhecida (40060), suprimindo mensagem de erro."
            )
            return
        if "already been acknowledged" in str(error).lower():
            print(
                f"[{command_name}] Interação já reconhecida, suprimindo mensagem de erro."
            )
            return

        print(f"Erro ao executar comando {command_name}: {error}")

        # Determina a mensagem de erro baseada no tipo de exceção
        if isinstance(error, HttpException):
            if error.status_code == 404:
                error_message = "❌ Recurso não encontrado. Verifique se a API está funcionando corretamente."
            elif error.status_code >= 500:
                error_message = "❌ Erro no servidor. Tente novamente mais tarde."
            elif error.status_code == 401:
                error_message = "❌ Não autorizado. Verifique suas credenciais."
            elif error.status_code == 403:
                error_message = "❌ Acesso negado."
            else:
                error_message = f"❌ Erro HTTP {error.status_code}: {error.message}"
        else:
            error_message = (
                "❌ Ocorreu um erro ao processar o comando. Tente novamente mais tarde."
            )

        # Verifica se já foi feito o defer/response
        try:
            if interaction.response.is_done():
                # Se já foi feito o defer, usa followup
                await interaction.followup.send(error_message, ephemeral=True)
            else:
                # Se ainda não foi feito, usa response
                await interaction.response.send(error_message, ephemeral=True)
        except Exception as e:
            print(f"Erro ao enviar mensagem de erro ao Discord: {e}")

    def _create_specific_callback(self, command: BotCommand):
        # Se não tem opções, cria callback simples
        if not command.options:

            async def callback(interaction: discord.Interaction):
                try:
                    await command.process(interaction)
                except Exception as e:
                    await self._handle_error(interaction, e, command.name)

            return callback

        # Se tem opções, cria callback com parâmetros específicos
        option_names = [opt.name for opt in command.options]

        if len(option_names) == 1:
            # Comando com 1 parâmetro - cria callback específico
            async def callback(interaction: discord.Interaction, name: str = ""):
                try:
                    await command.process(interaction, name)
                except Exception as e:
                    await self._handle_error(interaction, e, command.name)

            return callback
        else:
            # Comando com múltiplos parâmetros - cria callback com todos os parâmetros
            param_names = option_names
            if len(param_names) == 2:
                # Segundo parâmetro opcional (ex: /novomeme title description?)
                if not command.options[1].required:

                    async def callback(
                        interaction: discord.Interaction,
                        title: str,
                        description: Optional[str] = None,
                    ):
                        try:
                            await command.process(
                                interaction,
                                title=title,
                                description=description or "",
                            )
                        except Exception as e:
                            await self._handle_error(interaction, e, command.name)

                    return callback

                async def callback(
                    interaction: discord.Interaction, param1: str = "", param2: str = ""
                ):
                    try:
                        params = {param_names[0]: param1, param_names[1]: param2}
                        await command.process(interaction, **params)
                    except Exception as e:
                        await self._handle_error(interaction, e, command.name)

                return callback
            else:
                # Para mais de 2 parâmetros, usa abordagem genérica
                async def callback(interaction: discord.Interaction):
                    try:
                        await command.process(interaction)
                    except Exception as e:
                        await self._handle_error(interaction, e, command.name)

                return callback

    async def sync_commands(self, guild_id: Optional[int] = None) -> None:
        try:
            if guild_id:
                print(f"Sincronizando comandos para o servidor {guild_id}")
                synced = await self.tree.sync(guild=discord.Object(id=guild_id))
                for command in synced:
                    print(f"Comando {command.name} sincronizado (guild {guild_id})")
            synced = await self.tree.sync()
            for command in synced:
                print(f"Comando {command.name} sincronizado (global)")
        except Exception as e:
            print(f"Erro ao sincronizar comandos: {e}")
