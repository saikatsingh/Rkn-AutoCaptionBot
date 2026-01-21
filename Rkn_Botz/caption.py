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

# ⚠️ Please do not remove this credit!

from pyrogram import Client, filters, errors, types
from config import Rkn_Botz
from .database import rkn_botz
import asyncio, time, re, os, sys

@Client.on_message(filters.private & filters.user(Rkn_Botz.ADMIN) & filters.command("rknusers"))
async def show_user_stats(client, message):
    start = time.monotonic()
    rkn = await message.reply_text("🔍 Gathering bot statistics...")

    total = await rkn_botz.fetch_total_users()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))
    ping = (time.monotonic() - start) * 1000

    await rkn.edit_text(
        f"📊 <b>Bot Stats</b>\n\n"
        f"⏱️ <b>Uptime:</b> {uptime}\n"
        f"📡 <b>Ping:</b> <code>{ping:.2f} ms</code>\n"
        f"👤 <b>Total Users:</b> <code>{total}</code>"
    )
    
    
@Client.on_message(filters.private & filters.user(Rkn_Botz.ADMIN) & filters.command(["broadcast"]))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("❗ <b>Reply to a message to broadcast it to all users.</b>")

    rkn_status_msg = await message.reply("🔄 <b>Bot Processing...</b>\nChecking all registered users.")
    
    all_registered_users = await rkn_botz.list_all_users()
    total_users = len(all_registered_users)

    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for user_id in all_registered_users:
        try:
            await asyncio.sleep(0.5)
            await message.reply_to_message.copy(chat_id=user_id)
            success += 1
        except errors.InputUserDeactivated:
            deactivated += 1
            await rkn_botz.remove_user_by_id(user_id)
        except errors.UserIsBlocked:
            blocked += 1
            await rkn_botz.remove_user_by_id(user_id)
        except errors.FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            failed += 1
            continue

        try:
            await rkn_status_msg.edit(
                f"<u><b>📣 ʙʀᴏᴀᴅᴄᴀsᴛ ᴘʀᴏᴄᴇssɪɴɢ...</b></u>\n\n"
                f"• 👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs: <code>{total_users}</code>\n"
                f"• ✅ sᴜᴄᴄᴇssғᴜʟ: <code>{success}</code>\n"
                f"• ⛔ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: <code>{blocked}</code>\n"
                f"• 🗑️ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: <code>{deactivated}</code>\n"
                f"• ⚠️ ᴜɴsᴜᴄᴄᴇssғᴜʟ: <code>{failed}</code>"
            )
        except Exception:
            pass  # ignore edit failures during loop

    # Final status
    await rkn_status_msg.edit(
        f"<u><b>✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b></u>\n\n"
        f"• 👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs: <code>{total_users}</code>\n"
        f"• ✅ sᴜᴄᴄᴇssғᴜʟ: <code>{success}</code>\n"
        f"• ⛔ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: <code>{blocked}</code>\n"
        f"• 🗑️ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: <code>{deactivated}</code>\n"
        f"• ⚠️ ᴜɴsᴜᴄᴄᴇssғᴜʟ: <code>{failed}</code>"
    )

        
# Restart to cancell all process 
@Client.on_message(filters.private & filters.user(Rkn_Botz.ADMIN) & filters.command("restart"))
async def restart_bot(client, message):
    reply = await message.reply("🔄 Restarting bot...")
    await asyncio.sleep(3)
    await reply.edit("✅ Bot restarted successfully.")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
@Client.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    await rkn_botz.register_user(message.from_user.id)
    
    # Get random image from config
    await message.reply_photo(
        photo=Rkn_Botz.RKN_PIC,
        caption=(
            f"<b>Hey, {message.from_user.mention} 👋\n\n"
            f"I'm an Auto Caption Bot.\n"
            f"I auto-edit captions for videos, audio, documents posted in channels.\n\n"
            f"<b>⚡ Features:</b>\n"
            f"• Auto caption editing\n"
            f"• Batch edit messages\n"
            f"• Custom caption support\n"
            f"• Multi-language support\n\n"
            f"🔧 Use commands in channels where I'm admin.</b>"
        ),
        reply_markup=types.InlineKeyboardMarkup([
            [
                types.InlineKeyboardButton("➕ ADD ME", callback_data="add_me"),
                types.InlineKeyboardButton("🔄 UPDATE", callback_data="update_bot")
            ],
            [
                types.InlineKeyboardButton("💬 SUPPORT", callback_data="support"),
                types.InlineKeyboardButton("📘 HELP", callback_data="help")
            ],
            [
                types.InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")
            ]
        ])
    )


@Client.on_callback_query(filters.regex("^help$"))
async def help_cb(client, query):
    """Handle HELP button click"""
    await query.answer()
    
    help_text = (
        "<b>📘 HELP - Available Commands</b>\n\n"
        "<b>Caption Commands:</b>\n"
        "/set_caption - Set custom caption\n"
        "/delcaption - Delete custom caption\n\n"
        "<b>Batch Commands:</b>\n"
        "/batch_edit - Edit multiple messages\n\n"
        "<b>Features:</b>\n"
        "• Automatic caption editing\n"
        "• Batch message processing\n"
        "• Channel-specific settings\n"
        "• Multi-format support\n\n"
        "<b>Note:</b> Commands only work in channels where I'm admin."
    )
    
    await query.edit_message_text(
        text=help_text,
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("🏠 HOME", callback_data="start")],
            [types.InlineKeyboardButton("❌ CLOSE", callback_data="close")]
        ])
    )


@Client.on_callback_query(filters.regex("^about$"))
async def about_cb(client, query):
    """Handle ABOUT button click"""
    await query.answer()
    
    about_text = (
        "<b>ℹ️ BOT INFO</b>\n\n"
        "<b>📊 Statistics:</b>\n"
        f"👥 Users: {await rkn_botz.fetch_total_users()}\n\n"
        "<b>🤖 Bot Details:</b>\n"
        "Name: Auto Caption Bot\n"
        "Version: 2.0\n"
        "Creator: @RknDeveloper\n\n"
        "<b>✨ Features:</b>\n"
        "✅ Auto Caption Editing\n"
        "✅ Batch Processing\n"
        "✅ Multi-Language Support\n"
        "✅ Channel Management\n\n"
        "<b>📞 Support:</b>\n"
        "Channel: @Rkn_Bots_Updates\n"
        "Support: @Rkn_Bots_Support\n"
        "GitHub: RknDeveloper/Rkn-AutoCaptionBot"
    )
    
    await query.edit_message_text(
        text=about_text,
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("🏠 HOME", callback_data="start")],
            [types.InlineKeyboardButton("❌ CLOSE", callback_data="close")]
        ])
    )


@Client.on_callback_query(filters.regex("^add_me$"))
async def add_me_cb(client, query):
    """Handle ADD ME button click"""
    await query.answer("Click below to add me to your channel", show_alert=False)
    await query.edit_message_text(
        text="<b>➕ Add Bot to Channel</b>\n\nClick the link below to add me to your channel.",
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("➕ Add to Channel", url="https://t.me/Rkn_AutoCaption_Bot?startgroup=true")],
            [types.InlineKeyboardButton("🏠 HOME", callback_data="start")]
        ])
    )


@Client.on_callback_query(filters.regex("^update_bot$"))
async def update_bot_cb(client, query):
    """Handle UPDATE button click"""
    await query.answer("Check updates here", show_alert=False)
    await query.edit_message_text(
        text="<b>🔄 Bot Updates</b>\n\nVisit our channel for latest updates and features.",
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("📢 Updates Channel", url="https://t.me/Rkn_Bots_Updates")],
            [types.InlineKeyboardButton("🏠 HOME", callback_data="start")]
        ])
    )


@Client.on_callback_query(filters.regex("^support$"))
async def support_cb(client, query):
    """Handle SUPPORT button click"""
    await query.answer("Join support group", show_alert=False)
    await query.edit_message_text(
        text="<b>💬 Support Group</b>\n\nJoin our support group for help and queries.",
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("💬 Support Group", url="https://t.me/Rkn_Bots_Support")],
            [types.InlineKeyboardButton("🏠 HOME", callback_data="start")]
        ])
    )


@Client.on_callback_query(filters.regex("^start$"))
async def start_cb(client, query):
    """Handle HOME button click - return to start menu"""
    await query.answer()
    await query.edit_message_text(
        text=(
            f"<b>Hey, {query.from_user.mention} 👋\n\n"
            f"I'm an Auto Caption Bot.\n"
            f"I auto-edit captions for videos, audio, documents posted in channels.\n\n"
            f"<b>⚡ Features:</b>\n"
            f"• Auto caption editing\n"
            f"• Batch edit messages\n"
            f"• Custom caption support\n"
            f"• Multi-language support\n\n"
            f"🔧 Use commands in channels where I'm admin.</b>"
        ),
        reply_markup=types.InlineKeyboardMarkup([
            [
                types.InlineKeyboardButton("➕ ADD ME", callback_data="add_me"),
                types.InlineKeyboardButton("🔄 UPDATE", callback_data="update_bot")
            ],
            [
                types.InlineKeyboardButton("💬 SUPPORT", callback_data="support"),
                types.InlineKeyboardButton("📘 HELP", callback_data="help")
            ],
            [
                types.InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")
            ]
        ])
    )


@Client.on_callback_query(filters.regex("^close$"))
async def close_cb(client, query):
    """Handle CLOSE button click"""
    await query.answer()
    await query.message.delete()


# Batch edit command - edit multiple messages
@Client.on_message(filters.command("batch_edit") & filters.channel)
async def batch_edit(client, message):
    """Edit multiple messages in a channel
    Usage: /batch_edit <first_message_id> <last_message_id> <new_caption>
    """
    try:
        if len(message.command) < 2:
            return await message.reply("Usage: /batch_edit <first_msg_id> <last_msg_id> <caption>")
        
        parts = message.text.split(None, 3)
        if len(parts) < 4:
            return await message.reply("Usage: /batch_edit <first_msg_id> <last_msg_id> <caption>")
        
        try:
            first_msg_id = int(parts[1])
            last_msg_id = int(parts[2])
            new_caption = parts[3] if len(parts) > 3 else ""
        except ValueError:
            return await message.reply("Please provide valid message IDs")
        
        channel_id = message.chat.id
        status_msg = await message.reply(f"🔄 Processing {last_msg_id - first_msg_id + 1} messages...")
        
        success = 0
        failed = 0
        
        for msg_id in range(first_msg_id, last_msg_id + 1):
            try:
                await client.edit_message_caption(
                    chat_id=channel_id,
                    message_id=msg_id,
                    caption=new_caption
                )
                success += 1
            except Exception as e:
                failed += 1
                continue
            
            await asyncio.sleep(0.5)
        
        await status_msg.edit_text(
            f"✅ <b>Batch Edit Complete</b>\n\n"
            f"📤 Successfully edited: <code>{success}</code>\n"
            f"❌ Failed: <code>{failed}</code>"
        )
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


# this command works on channels only 
@Client.on_message(filters.command("set_caption") & filters.channel)
async def set_caption(client, message):
        try:
                    member = await client.get_chat_member(message.chat.id, client.me.id)
                    if member.status not in ['administrator', 'creator']:
                return await message.reply(f"❌ I need to be admin in this channel to set captions.")
    except Exception:
        return await message.reply('❌ Error: I need to be admin in this channel.')
    if len(message.command) < 2:
        return await message.reply("Usage: /set_caption <your caption>\nUse `{file_name}` or `{caption}`.")

    caption = message.text.split(" ", 1)[1]
    channel_id = message.chat.id

    existing = await rkn_botz._channels_collection.find_one({"channelId": channel_id})
    if existing:
        await rkn_botz.update_channel_caption(channel_id, caption)
    else:
        await rkn_botz.add_channel_caption(channel_id, caption)

    await message.reply(f"✅ Caption set:\n\n<code>{caption}</code>")


# this command works on channels only 
@Client.on_message(filters.command(["delcaption", "del_caption", "delete_caption"]) & filters.channel)
async def delete_caption(client, message):
    channel_id = message.chat.id
    result = await rkn_botz._channels_collection.delete_one({"channelId": channel_id})
    if result.deleted_count:
        await message.reply("🗑️ Caption deleted. Using default now.")
    else:
        await message.reply("ℹ️ No caption found.")


def detect_year(file_name):
    # Step 1: Clean filename (replace symbols with space)
    clean_name = re.sub(r"[^\d]", " ", file_name)

    # Step 2: Extract all 4-digit sequences
    candidates = re.findall(r"\b\d{4}\b", clean_name)

    # Step 3: Return the first one that matches year range
    for year in candidates:
        year_int = int(year)
        if 1900 <= year_int <= 2099:
            return year # results years
            
    return "Unknown" # not available 
    
def detect_season(file_name):
    match = re.search(r'\bS(\d{2})\b', file_name, re.IGNORECASE)
    return int(match.group(1)) if match else "Unknown"

def detect_episode(file_name):
    match = re.search(r'\bE(\d{2})\b', file_name, re.IGNORECASE)
    return int(match.group(1)) if match else "Unknown"
    
def detect_quality(file_name):
    match = re.search(r'\b(2160p|1440p|1080p|720p|480p|360p|240p)\b', file_name.lower())
    return match.group(1) if match else "Unknown"
    
def detect_language(file_name):
    languages = ['hindi', 'english', 'telugu', 'tamil', 'malayalam', 'kannada', 'bengali', 'marathi', 'urdu']
    for lang in languages:
        if re.search(rf'\b{lang}\b', file_name, re.IGNORECASE):
            return lang.capitalize()
            
    return "Unknown"
    

def convert_size(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'
    
@Client.on_message(filters.channel)
async def auto_caption(client, message):
    if not message.media:
        return

    for mtype in ("video", "audio", "document", "voice"):
        media = getattr(message, mtype, None)
        if media and hasattr(media, "file_name"):
            file_name = re.sub(r"@\w+", "", media.file_name or "").replace("_", " ").replace(".", " ").strip()
            file_size = getattr(media, "file_size", None)  # ✅ file_size added here
            break
    else:
        return

    channel_id = message.chat.id
    cap_data = await rkn_botz._channels_collection.find_one({"channelId": channel_id})
    original_caption = message.caption or file_name

    try:
        if cap_data:
            custom_caption = cap_data.get("caption", "")
            formatted = custom_caption.format(
                file_name=file_name,
                caption=original_caption,
                language=detect_language(original_caption),
                episode=detect_episode(original_caption),
                season=detect_season(original_caption),
                year=detect_year(original_caption),
                quality=detect_quality(original_caption),
                file_size=convert_size(file_size) if file_size else "Unknown"  # ✅ Fixed
            )
        else:
            formatted = Rkn_Botz.DEFAULT_CAPTION.format(
                file_name=file_name,
                caption=original_caption,
                language=detect_language(original_caption),
                episode=detect_episode(original_caption),
                season=detect_season(original_caption),
                year=detect_year(original_caption),
                file_size=convert_size(file_size) if file_size else "Unknown"  # ✅ Fixed
            )
        await message.edit_caption(formatted)
    except errors.FloodWait as e:
        await asyncio.sleep(e.value)


# ======== HELP MENU CALLBACKS ========

# Dictionary for help menu message
@Client.on_callback_query(filters.regex(r'^help_'))
async def help_menu_handler(client, query):
    """Generic handler for all help menu buttons"""
    await query.answer()
    button_name = query.data.replace('help_', '')
    
    # Help menu messages
    help_messages = {
        'caption': '<b>📝 CAPTION MANAGEMENT</b>\nCustomize your channel caption format.\n\n<b>Commands:</b>\n/set_cap - Set custom caption\n/del_cap - Delete caption',
        'font': '<b>🎨 FONT STYLING</b>\nUse HTML tags: <b>Bold</b>, <i>Italic</i>, <u>Underline</u>',
        'language': '<b>🌐 LANGUAGE</b>\n/set_language Hindi|English|Tamil',
        'quality': '<b>🎬 QUALITY</b>\n/set_quality WEB-DL|BluRay|HDTV',
        'username': '<b>👤 USERNAME</b>\n/remove_usernames on/off',
        'links': '<b>🔗 LINKS</b>\n/remove_links on/off',
        'blacklist': '<b>🚫 BLACKLIST</b>\n/blacklist_words term1|term2',
        'emoji': '<b>😊 EMOJI</b>\n/remove_emoji on/off',
        'replace_word': '<b>🔄 REPLACE</b>\n/replace_words old:new',
        'remove_word': '<b>🗑️ REMOVE WORDS</b>\n/remove_words word1|word2',
        'prefix': '<b>🔠 PREFIX</b>\n/set_prefix [TEXT]',
        'suffix': '<b>🔚 SUFFIX</b>\n/set_suffix [TEXT]',
        'symbol': '<b>🔣 SYMBOLS</b>\n/remove_symbols \"symbols\"',
        'space_line': '<b>📐 SPACE & LINE</b>\n/rem_space_line on/off',
        'button': '<b>🔘 BUTTONS</b>\n/set_buttons [V] Text | [H] Text',
        'extension': '<b>💾 EXTENSION</b>\n/fix_extension on/off',
        'details': '<b>⚙️ SETTINGS</b>\n/show_details',
        'reset': '<b>🔄 RESET</b>\n/reset_all',
        'copy_setting': '<b>📨 COPY</b>\n/get_settings | /apply_settings',
        'batch_edit': '<b>🗃️ BATCH EDIT</b>\n/batch_edit'
    }
    
    message_text = help_messages.get(button_name, '<b>Help</b>\nFeature coming soon!')
    
    await query.edit_message_text(
        text=message_text,
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton('🔙 Back', callback_data='help')],
            [types.InlineKeyboardButton('❌ Exit', callback_data='close')]
        ])
    
    @Client.on_callback_query(filters.regex("^add_me$"))
async def add_me_cb(client, query):
    """Handle ADD ME button click"""
    await query.answer()
    invite_link = await client.export_chat_invite_link(query.message.chat.id)
    await query.edit_message_text(
        text="<b>➡️ Add Bot to Channel</b>\n\nClick below to add me to your channel.",
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("➡️ Add to Channel", url="https://t.me/Rkn_AutoCaption_Bot?startgroup=true")],
            [types.InlineKeyboardButton("🎱 HOME", callback_data="start")]
        ])

@Client.on_callback_query(filters.regex("^update_bot$"))
async def update_bot_cb(client, query):
    """Handle UPDATE button click"""
    await query.answer()
    await query.edit_message_text(
        text="<b>🔄 Bot Updates</b>\n\nVisit our channel for latest updates and features.",
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("📢 Updates Channel", url="https://t.me/Rkn_Bots_Updates")],
            [types.InlineKeyboardButton("🎱 HOME", callback_data="start")]
        ])
    )

@Client.on_callback_query(filters.regex("^support$"))
async def support_cb(client, query):
    """Handle SUPPORT button click"""
    await query.answer()
    await query.edit_message_text(
        text="<b>💬 Support Group</b>\n\nJoin our support group for help and queries.",
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("💬 Support Group", url="https://t.me/Rkn_Bots_Support")],
            [types.InlineKeyboardButton("🎱 HOME", callback_data="start")]
        ])
    )
