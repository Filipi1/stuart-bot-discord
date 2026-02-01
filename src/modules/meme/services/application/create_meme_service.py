import asyncio
import io
import uuid
import discord
from typing import Dict, Optional, Any

from modules.meme.services.application.get_memes_count import (
    GetMemesCountApplicationService,
)
from modules.meme.services.domain.create_meme_service import CreateMemeDomainService
from modules.shared.adapters import ApplicationService
from modules.shared.services.image.image_service import ImageService
from modules.shared.services.requests.exceptions import HttpException
from modules.shared.utils.discord_utils import DiscordUtils


VALID_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")
VALID_CONTENT_TYPES = ("image/jpeg", "image/png", "image/jpg")
IMAGE_WAIT_TIMEOUT = 60


class CreateMemeApplicationService(ApplicationService):
    def __init__(
        self,
        create_meme_domain_service: CreateMemeDomainService,
        image_service: ImageService,
        get_memes_count: GetMemesCountApplicationService,
    ):
        self.__create_meme_domain = create_meme_domain_service
        self.__image_service = image_service
        self.__get_memes_count = get_memes_count
        self._pending: Dict[str, Dict[str, Any]] = {}
        super().__init__(CreateMemeApplicationService.__name__)

    async def process(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
    ) -> None:
        await interaction.response.send_message(
            "📷 Manda a imagem aí no chat! JPG ou PNG, e corre que são 60 segundos 😏",
            ephemeral=False,
        )

        try:
            message = await interaction.client.wait_for(
                "message",
                check=lambda message: DiscordUtils.is_from_interaction_user(
                    message, interaction
                ),
                timeout=IMAGE_WAIT_TIMEOUT,
            )
        except asyncio.TimeoutError:
            await interaction.followup.send(
                "Eita, deu tempo! 😅 Manda de novo com /novomeme",
                ephemeral=True,
            )
            return

        attachment = DiscordUtils.get_image_attachment(message)
        if not attachment:
            await interaction.followup.send(
                "Cadê a imagem? 😂 Manda uma em JPG ou PNG aí!",
                ephemeral=True,
            )
            return

        image_bytes = await self.__image_service.download_image(attachment.url)
        await message.delete()
        pending_id = str(uuid.uuid4())
        self.register_pending(
            pending_id,
            {
                "title": title,
                "description": description,
                "user_id": interaction.user.id,
                "url": attachment.url,
                "filename": attachment.filename,
                "content_type": attachment.content_type,
                "user_message_id": message.id,
                "image_bytes": image_bytes,
            },
        )

        embed = self.build_preview_embed(
            title=title,
            description=description,
            attachment_filename=attachment.filename,
        )
        view = DiscordUtils.build_view(
            buttons=[
                discord.ui.Button(
                    label="Confirmar Envio",
                    style=discord.ButtonStyle.success,
                    custom_id=f"novomeme_confirm_{pending_id}",
                ),
                discord.ui.Button(
                    label="Cancelar",
                    style=discord.ButtonStyle.danger,
                    custom_id=f"novomeme_cancel_{pending_id}",
                ),
            ],
        )
        file = discord.File(fp=io.BytesIO(image_bytes), filename=attachment.filename)
        await interaction.followup.send(
            embed=embed, view=view, file=file, ephemeral=False
        )
        try:
            first_message = await interaction.original_response()
            await first_message.delete()
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

    def register_pending(self, pending_id: str, data: Dict[str, Any]) -> None:
        self._pending[pending_id] = data

    def get_pending_data(self, pending_id: str) -> Optional[Dict[str, Any]]:
        return self._pending.get(pending_id)

    def consume_pending(self, pending_id: str) -> Optional[Dict[str, Any]]:
        return self._pending.pop(pending_id, None)

    def build_preview_embed(
        self,
        title: str,
        description: str,
        attachment_filename: str,
    ) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=0xFF6B6B,
        )
        embed.set_image(url=f"attachment://{attachment_filename}")
        embed.set_footer(text="Tá certo? Confirma ou manda cancelar 👇")
        return embed

    async def handle_confirm(self, interaction: discord.Interaction) -> None:
        if not DiscordUtils.is_button_from_interaction_user(
            "novomeme_confirm_", interaction
        ):
            return
        pending_id = interaction.data.get("custom_id", "") if interaction.data else ""
        pending_id = pending_id[len("novomeme_confirm_") :]
        data = self.get_pending_data(pending_id)
        if not data:
            await self._respond_ephemeral(
                interaction, "Essa já era... expirou ou alguém já usou. Manda outra! 🔄"
            )
            await self._delete_message_silent(interaction.message)
            return
        if data.get("user_id") != interaction.user.id:
            await self._respond_ephemeral(
                interaction, "Só quem criou pode confirmar essa, hein 😏"
            )
            return
        self.consume_pending(pending_id)

        await interaction.response.defer(ephemeral=False)
        await interaction.message.edit(
            content="Segura aí, tô mandando... 🚀",
            embed=None,
            view=None,
            attachments=[],
        )

        try:
            desc = data.get("description")
            await self.__create_meme_domain.process(
                title=data["title"],
                description=desc if desc else None,
                image_bytes=data["image_bytes"],
                image_filename=data["filename"],
                content_type=data.get("content_type", "image/jpeg"),
            )
        except HttpException as e:
            self.logger.error(f"API error: {e.status_code} - {e.message}")
            error_message = "Deu ruim pra enviar 😅 Tenta de novo daqui a pouco!"
            try:
                await interaction.message.edit(
                    content=error_message,
                    embed=None,
                    view=None,
                    attachments=[],
                )
            except discord.NotFound:
                await interaction.followup.send(
                    error_message,
                    ephemeral=True,
                )
            return
        except Exception as e:
            self.logger.error(str(e))
            try:
                await interaction.message.edit(
                    content=error_message,
                    embed=None,
                    view=None,
                    attachments=[],
                )
            except discord.NotFound:
                await interaction.followup.send(
                    error_message,
                    ephemeral=True,
                )
            return

        try:
            await interaction.message.edit(
                content="🎉 Meme criado, agora é só digitar o /eusou e descobrir quem você é!",
                embed=None,
                view=None,
                attachments=[],
            )
        except discord.NotFound:
            await interaction.followup.send(
                "🎉 Meme criado, agora é só digitar o /eusou e descobrir quem você é!",
                ephemeral=False,
            )

        try:
            memes_count = await self.__get_memes_count.process()
            activity = discord.CustomActivity(name=f"{memes_count} memes")
            await interaction.client.change_presence(activity=activity)
        except Exception:
            pass

    async def handle_cancel(self, interaction: discord.Interaction) -> None:
        if not DiscordUtils.is_button_from_interaction_user(
            "novomeme_cancel_", interaction
        ):
            return
        pending_id = interaction.data.get("custom_id", "") if interaction.data else ""
        pending_id = pending_id[len("novomeme_cancel_") :]
        data = self.get_pending_data(pending_id)
        if not data:
            await self._respond_ephemeral(
                interaction, "Essa já era... expirou ou alguém já usou. Manda outra! 🔄"
            )
            await self._delete_message_silent(interaction.message)
            return
        if data.get("user_id") != interaction.user.id:
            await self._respond_ephemeral(
                interaction, "Só quem criou pode cancelar essa 😏"
            )
            return
        self.consume_pending(pending_id)

        await interaction.response.defer(ephemeral=False)
        try:
            await interaction.message.edit(
                content="Beleza, cancelado! 👍",
                embed=None,
                view=None,
                attachments=[],
            )
        except discord.NotFound:
            await interaction.followup.send("Beleza, cancelado! 👍", ephemeral=False)

    async def _respond_ephemeral(
        self, interaction: discord.Interaction, message: str
    ) -> None:
        try:
            if interaction.response.is_done():
                await interaction.followup.send(message, ephemeral=True)
            else:
                await interaction.response.send_message(message, ephemeral=True)
        except discord.NotFound:
            pass

    async def _delete_message_silent(self, message: discord.Message) -> None:
        try:
            await message.delete()
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass
