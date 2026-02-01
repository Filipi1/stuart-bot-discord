import discord
from modules.shared.adapters import BotCommand
from modules.shared.dataclasses import CommandOption
from container import container


class NovoMemeCommand(BotCommand):
    def __init__(self):
        self.create_meme_service = container.create_meme
        super().__init__(
            name="novomeme",
            description="Criar um novo meme",
            options=[
                CommandOption(
                    name="title",
                    description="Título do meme",
                    required=True,
                ),
                CommandOption(
                    name="description",
                    description="Descrição do meme",
                    required=False,
                ),
            ],
        )

    async def process(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
    ) -> None:
        await self.create_meme_service.process(interaction, title, description or "")
