import platform
import time
from sys import version as pyver

import psutil
from Music import Music_START_TIME, app, SUDOERS
from Music.MusicUtilities.database.chats import get_served_chats
from Music.MusicUtilities.database.gbanned import get_gbans_count
from Music.MusicUtilities.database.sudo import get_sudoers
from Music.MusicUtilities.helpers.time import get_readable_time
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pytgcalls import __version__ as pytover


@app.on_message(filters.user(SUDOERS) & filters.command("stats") & ~filters.edited)
async def gstats(_, message):
    m = await message.reply_text("**Getting Stats**\n\nPlease wait for some time..")
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    blocked = await get_gbans_count()
    sudoers = await get_sudoers()
    j = 0
    for count, user_id in enumerate(sudoers, 0):
        try:
            await app.get_users(user_id)
            j += 1
        except Exception:
            continue
    modules_count = "17"
    sc = platform.system()
    arch = platform.machine()
    ram = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
    bot_uptime = int(time.time() - Music_START_TIME)
    uptime = f"{get_readable_time((bot_uptime))}"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0 ** 3)
    total = str(total)
    used = hdd.used / (1024.0 ** 3)
    used = str(used)
    free = hdd.free / (1024.0 ** 3)
    free = str(free)
    msg = f"""
**Global Stats of Private Music Bot**:\n\n
[•]<u>__**System Stats**__</u>
**Music Uptime:** {uptime}
**System Process:** Online
**Platform:** {sc}
**Storage:** Used {used[:4]} GiB out of {total[:4]} GiB, free {free[:4]} GiB
**Architecture:** {arch}
**Ram:** {ram}
**Python Version:** {pyver.split()[0]}
**Pyrogram Version:** {pyrover}
**PyTgCalls Version:** {pytover.__version__}

[•]<u>__**Bot Stats**__</u>
**Modules Loaded:** {modules_count}
**GBanned Users:** {blocked}
**Sudo Users:** {j}
**Allowed Chats:** {len(served_chats)}

"""
    served_chats.pop(0)
    await m.edit(msg, disable_web_page_preview=True)
