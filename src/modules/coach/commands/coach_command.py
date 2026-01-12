import discord
from modules.shared.adapters import BotCommand
from container import container


class CoachCommand(BotCommand):
    def __init__(self):
        self.get_coach_service = container.get_coach
        super().__init__(
            name="coach",
            description="Comando para sortear coach",
            options=[],
        )

    async def process(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        embed = await self.get_coach_service.process()
        await interaction.followup.send(embed=embed, ephemeral=False)
