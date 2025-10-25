import discord
from modules.shared.adapters import BotCommand
from modules.shared.dataclasses.command_option import CommandOption


class CoachCommand(BotCommand):
    def __init__(self):
        super().__init__(name="coach", description="Comando para sortear coach", options=[
            CommandOption(name="name", description="Seu nome", required=True)
        ])

    async def process(self, interaction: discord.Interaction, name: str) -> None:
        try:
            await interaction.response.defer()
            embed = discord.Embed(
                title="🎲 Coach Sorteado!",
                description=f"**Título:** Coach de {name}\n**Descrição:** Este é um coach de {name} para demonstração",
                color=0xff6b6b
            )
            
            embed.add_field(
                name="🎯 Resultado",
                value="Você foi sorteado! Este coach agora é seu!",
                inline=False
            )
            
            embed.set_footer(text=f"Sorteado para {interaction.user.display_name}")
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
            
        except Exception as e:
            print(f"Erro ao sortear coach: {e}")
            await interaction.response.send_message(
                "❌ Ocorreu um erro ao sortear o coach. Tente novamente mais tarde.",
                ephemeral=True
            )
