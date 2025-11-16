import discord
from modules.shared.adapters import BotCommand
from container import container


class IamCommand(BotCommand):
    def __init__(self):
        self.get_meme_service = container.get_meme
        super().__init__(
            name="eusou", description="Comando para sortear memes", options=[]
        )

    async def process(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        embed = await self.get_meme_service.process(interaction.user.name)
        await interaction.followup.send(embed=embed, ephemeral=False)
