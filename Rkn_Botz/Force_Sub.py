# AutoCaptionBot by RknDeveloper
# Copyright (c) 2024 RknDeveloper
# Licensed under the MIT License
# https://github.com/RknDeveloper/Rkn-AutoCaptionBot/blob/main/LICENSE

# Please retain this credit when using or forking this code.

# Developer Contacts:
# Telegram: @RknDeveloperr
# Updates Channel: @Rkn_Bots_Updates & @Rkn_Botz
# Special Thanks To: @ReshamOwner
# Update Channels: @Digital_Botz & @DigitalBotz_Support

# Please do not remove this credit!

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant

from config import Rkn_Botz as Config
from .database import rkn_botz


# Check if FORCE_SUB is enabled
if Config.FORCE_SUB:
    # Async callable filter class
    class ForceSubCheck:
        def __init__(self, channel: str):
            self.channel = channel.lstrip("@")

        async def __call__(self, _, client: Client, message: Message) -> bool:
            user_id = message.from_user.id

            # Register user in DB if not already
            await rkn_botz.register_user(user_id)

            if not self.channel:
                # ForceSub off
                return False

            try:
                member = await client.get_chat_member(self.channel, user_id)
                # True => filter pass korbe jodi LEFT/BANNED, mane force sub lagbe
                return member.status in [
                    enums.ChatMemberStatus.LEFT,
                    enums.ChatMemberStatus.BANNED,
                ]
            except UserNotParticipant:
                return True
            except Exception:
                return False

    # Handler for blocked users / unsubscribed
    @Client.on_message(filters.private & filters.create(ForceSubCheck(Config.FORCE_SUB), name="force_sub_filter"))
    async def handle_force_sub(client: Client, message: Message):
        user_id = message.from_user.id
        chat_link = f"https://t.me/{Config.FORCE_SUB.lstrip('@')}"

        # Button UI
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔔 Join Update Channel", url=chat_link)]]
        )

        try:
            member = await client.get_chat_member(Config.FORCE_SUB, user_id)
            if member.status == enums.ChatMemberStatus.BANNED:
                return await message.reply_text(
                    "**🚫 You are banned from using this bot.\nContact admin if this is a mistake.**"
                )
        except UserNotParticipant:
            pass
        except Exception as e:
            return await message.reply_text(f"⚠️ Unexpected error: `{e}`")

        # Default reply if not joined
        return await message.reply_text(
            "**Hey buddy! 🔐 You need to join our updates channel before using me.**",
            reply_markup=button,
        )
else:
    # If FORCE_SUB is disabled, create a dummy handler that allows all messages
    @Client.on_message(filters.private)
    async def handle_no_force_sub(client: Client, message: Message):
        # Register user in DB
        await rkn_botz.register_user(message.from_user.id)
        # Pass through, don't block anything


# ————
# End of file
# Original author: @RknDeveloperr
# Telegram: @RknDeveloperr
# Updates: @Rkn_Bots_Updates & @Rkn_Botz
# Please do not remove this credit!
