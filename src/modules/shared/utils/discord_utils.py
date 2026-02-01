import discord


class DiscordUtils:
    VALID_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")
    VALID_CONTENT_TYPES = ("image/jpeg", "image/png", "image/jpg")

    @staticmethod
    def is_button_from_interaction_user(
        custom_id: str, interaction: discord.Interaction
    ) -> bool:
        interaction_custom_id = (
            interaction.data.get("custom_id", "") if interaction.data else ""
        )
        if not interaction_custom_id.startswith(custom_id):
            return False
        return True

    @staticmethod
    def is_from_interaction_user(
        message: discord.Message, interaction: discord.Interaction
    ) -> bool:
        if message.author.id != interaction.user.id:
            return False
        if message.channel.id != interaction.channel.id:
            return False
        return True

    @staticmethod
    def get_image_attachment(message: discord.Message) -> discord.Attachment | None:
        if not message.attachments:
            return None
        if not DiscordUtils.is_valid_image_attachment(message.attachments[0]):
            return None
        return message.attachments[0]

    @staticmethod
    def is_valid_image_attachment(attachment: discord.Attachment) -> bool:
        if not attachment.filename:
            return False
        ext_idx = attachment.filename.lower().rfind(".")

        if ext_idx == -1:
            return False

        if (
            attachment.filename[ext_idx:].lower()
            not in DiscordUtils.VALID_IMAGE_EXTENSIONS
        ):
            return False

        if (
            attachment.content_type
            and attachment.content_type.lower() not in DiscordUtils.VALID_CONTENT_TYPES
        ):
            return False
        return True

    @staticmethod
    def build_view(
        buttons: list[discord.ui.Button], timeout: float | None = 180
    ) -> discord.ui.View:
        view = discord.ui.View(timeout=timeout)
        for button in buttons:
            view.add_item(button)
        return view
