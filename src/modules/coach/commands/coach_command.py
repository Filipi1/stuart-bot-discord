import discord
from modules.shared.adapters import BotCommand
from modules.shared.dataclasses.command_option import CommandOption


class CoachCommand(BotCommand):
    def __init__(self):
        super().__init__(
            name="coach",
            description="Comando para sortear coach",
            options=[CommandOption(name="name", description="Seu nome", required=True)],
        )

    async def process(self, interaction: discord.Interaction, name: str) -> None:
        try:
            await interaction.response.defer()
            embed = discord.Embed(
                title="🕝 - Em Breve",
                color=0xFF6B6B,
            )
            await interaction.followup.send(embed=embed, ephemeral=False)

        except Exception as e:
            print(f"Erro ao sortear coach: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ Ocorreu um erro ao sortear o coach. Tente novamente mais tarde.",
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    "❌ Ocorreu um erro ao sortear o coach. Tente novamente mais tarde.",
                    ephemeral=True,
                )
