import discord
from modules.shared.services import CommandRegistrationService
from modules.shared.settings.settings import Settings
from container import container


class StuartBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_service = CommandRegistrationService(self)

    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        self.command_service.register_all_commands()
        memes_count = await container.get_memes_count.process()
        activity = discord.CustomActivity(name=f"{memes_count} memes")
        await self.change_presence(activity=activity)
        await self.command_service.sync_commands()

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
client.run(Settings().BOT_TOKEN)
