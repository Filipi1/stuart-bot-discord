import discord
from modules.shared.services import CommandRegistrationService
from modules.shared.services.health_check_server import start_health_check_server
from modules.shared.settings.settings import Settings
from container import container


class StuartBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_service = CommandRegistrationService(self)

    async def setup_hook(self):
        self.command_service.register_all_commands()
        await self.command_service.sync_commands(guild_id=container.discord_guild_id)

    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        memes_count = await container.get_memes_count.process()
        activity = discord.CustomActivity(name=f"{memes_count} memes")
        await self.change_presence(activity=activity)

    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            custom_id = (interaction.data or {}).get("custom_id", "")
            if custom_id.startswith("novomeme_confirm_"):
                await container.create_meme.handle_confirm(interaction)
            elif custom_id.startswith("novomeme_cancel_"):
                await container.create_meme.handle_cancel(interaction)

    async def on_message(self, message):
        if str(self.user.id) not in str(message.content):
            return

        try:
            print(f"Message from {message.author}: {message.content}")
        except UnicodeEncodeError:
            print(f"Message from {message.author}: [conteudo com caracteres especiais]")


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = StuartBot(intents=intents)
settings = Settings()
start_health_check_server(port=settings.PORT)
client.run(settings.BOT_TOKEN)
