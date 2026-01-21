# AutoCaptionBot by RknDeveloper
# Copyright (c) 2024 RknDeveloper
# Licensed under the MIT License
# https://github.com/RknDeveloper/Rkn-AutoCaptionBot/blob/main/LICENSE

# ⚠️ Please do not remove this credit!

import os
import time


class Rkn_Botz(object):
    # Rkn client config (required)
    # 👉 ei 3 ta Koyeb env-e must set korbe
    API_ID = int(os.environ.get("API_ID", "29563132"))
    API_HASH = os.environ.get("API_HASH", "b39be032fc0c567d0cda60dbea99606e")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # Start pic (default image link) – chaile env diye change korte parbe
    RKN_PIC = os.environ.get(
        "RKN_PIC",
        "https://graph.org/file/60c098107c0b0ef533bb4-5db20bb1ba846f2a5f.jpg"
    )

    # Bot uptime (start time)
    BOT_UPTIME = time.time()

    # Server port (default 8080)
    PORT = int(os.environ.get("PORT", "8080"))

    # Force subscribe channel username (without @)
    # example: FORCE_SUB=creazy_updates_zone
    FORCE_SUB = os.environ.get("FORCE_SUB", "creazy_updates_zone")

    # Database config (required)
    DB_NAME = os.environ.get("DB_NAME", "AutoCaption_V05_Bot")
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://workwithsaikat:saikat9735@cluster0.0e5vp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # Default caption (with safe fallback)
    # 👉 ekhane sob variable use korte parbi: {file_name}, {default_caption}, {resolution}, {quality}, {audio}, {language}, {file_size}, {year}, {season}, {episode}, {ott}, {lib}, {extension}, {fps}, {bitrate}, {shortsub}
    DEFAULT_CAPTION = os.environ.get(
        "DEFAULT_CAPTION",
        "**{file_name}\n\n📢 Main Channel: @creazy_updates_zone**"
    )

    # Sticker ID default
    STICKER_ID = os.environ.get(
        "STICKER_ID",
        "CAACAgIAAxkBAAELFqBllhB70i13m-woXeIWDXU6BD2j7wAC9gcAAkb7rAR7xdjVOS5ziTQE"
    )

    # Admin ID (single integer)
    # 👉 ekhane nijer Telegram numeric ID env-e ADMIN hishebe dibe
    ADMIN = int(os.environ.get("ADMIN", "0"))


# ————
# End of file
# Original author: @RknDeveloperr
# Telegram: @RknDeveloperr
# Updates: @Rkn_Bots_Updates & @Rkn_Botz
# ⚠️ Please do not remove this credit!

