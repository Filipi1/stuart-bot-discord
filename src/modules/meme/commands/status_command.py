import discord
from modules.shared.adapters import BotCommand
from container import container


class StatusCommand(BotCommand):
    def __init__(self):
        self.get_memes_status_service = container.get_memes_status
        super().__init__(
            name="info", description="Informações sobre o status dos memes", options=[]
        )

    async def process(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        embed = await self.get_memes_status_service.process()
        await interaction.followup.send(embed=embed, ephemeral=False)
