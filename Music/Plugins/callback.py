import asyncio
import os
import random
import re
import time as sedtime
from asyncio import QueueEmpty
from time import time

import yt_dlp
from Music import aiohttpsession as session
from Music import app
from Music.MusicUtilities.database.queue import (
    is_active_chat,
    is_music_playing,
    music_off,
    music_on,
    remove_active_chat,
)
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.gets import themes
from Music.MusicUtilities.helpers.inline import audio_markup, play_keyboard, play_markup
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.MusicUtilities.tgcallsrun import (
    clear,
    convert,
    download,
    get,
    is_empty,
    music,
    task_done,
)
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls.types.input_stream import InputAudioStream, InputStream

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")

flex = {}


async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False


@Client.on_callback_query(filters.regex(pattern=r"ppcl"))
async def closesmex(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    CallbackQuery.from_user.id
    try:
        smex, user_id = callback_request.split("|")
    except Exception as e:
        await CallbackQuery.message.edit(
            f"""
Terjadi kesalahan
Kemungkinan alasannya bisa** :{e}
"""
        )
        return
    if CallbackQuery.from_user.id != int(user_id):
        await CallbackQuery.answer(
            "Anda tidak diizinkan untuk menutup memu ini", show_alert=True
        )
        return
    await CallbackQuery.message.delete()
    await CallbackQuery.answer()


@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Anda tidak memiliki izin yang diperlukan untuk melakukan tindakan ini.\n• ❌ MENGELOLA OBROLAN SUARA",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music.pytgcalls.pause_stream(chat_id)
            await music_off(chat_id)
            await CallbackQuery.answer("Voicechat Paused", show_alert=True)
            user_id = CallbackQuery.from_user.id
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.message.reply(
                f"🎧 Lagu Dijeda oleh {rpk}!", reply_markup=play_keyboard
            )
            await CallbackQuery.message.delete()
        else:
            await CallbackQuery.answer(f"Tidak ada yang diputar!", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"Tidak ada yang diputar di Musik!", show_alert=True)


@Client.on_callback_query(filters.regex("resumevc"))
async def resumevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Anda tidak memiliki izin yang diperlukan untuk melakukan tindakan ini.

• ❌ MENGELOLA OBROLAN SUARA
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer(
                "Saya tidak berpikir jika ada sesuatu yang dijeda di obrolan suara",
                show_alert=True,
            )
            return
        else:
            await music_on(chat_id)
            await music.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer("Dilanjutkan", show_alert=True)
            user_id = CallbackQuery.from_user.id
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.message.reply(
                f"🎧 Lagu Dilanjutkan oleh {rpk}!", reply_markup=play_keyboard
            )
            await CallbackQuery.message.delete()
    else:
        await CallbackQuery.answer(f"Tidak ada yang diputar!", show_alert=True)


@Client.on_callback_query(filters.regex("skipvc"))
async def skipvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Anda tidak memiliki izin yang diperlukan untuk melakukan tindakan ini

• ❌ MENGELOLA OBROLAN SUARA
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
        task_done(chat_id)
        if is_empty(chat_id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id)
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await remove_active_chat(chat_id)
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(
                f"""
**Tombol Lewati Digunakan Oleh** {rpk}

Tidak ada lagi lagu di Antrian

Meninggalkan Obrolan Suara
"""
            )
            await music.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await CallbackQuery.answer("Obrolan Suara Dilewati", show_alert=True)
            afk = get(chat_id)["file"]
            f1 = afk[0]
            f2 = afk[1]
            f3 = afk[2]
            finxx = f"{f1}{f2}{f3}"
            if str(finxx) != "raw":
                mystic = await CallbackQuery.message.reply(
                    """
Musik sedang diputar Daftar Putar....

Mengunduh Musik Berikutnya Dari Daftar Putar....
"""
                )
                url = f"https://www.youtube.com/watch?v={afk}"
                try:
                    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                        x = ytdl.extract_info(url, download=False)
                except Exception as e:
                    return await mystic.edit(
                        f"""
Gagal mengunduh video ini.

**Alasan**:{e}
"""
                    )
                title = x["title"]
                videoid = afk

                def my_hook(d):
                    if d["status"] == "downloading":
                        percentage = d["_percent_str"]
                        per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                        per = int(per)
                        eta = d["eta"]
                        speed = d["_speed_str"]
                        size = d["_total_bytes_str"]
                        bytesx = d["total_bytes"]
                        if str(bytesx) in flex:
                            pass
                        else:
                            flex[str(bytesx)] = 1
                        if flex[str(bytesx)] == 1:
                            flex[str(bytesx)] += 1
                            sedtime.sleep(1)
                            mystic.edit(
                                f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        if per > 500:
                            if flex[str(bytesx)] == 2:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(
                                    f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                                )
                                print(
                                    f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds"
                                )
                        if per > 800:
                            if flex[str(bytesx)] == 3:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(
                                    f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                                )
                                print(
                                    f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds"
                                )
                        if per == 1000:
                            if flex[str(bytesx)] == 4:
                                flex[str(bytesx)] = 1
                                sedtime.sleep(0.5)
                                mystic.edit(
                                    f"Downloading {title[:50]}.....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                                )
                                print(
                                    f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds"
                                )

                loop = asyncio.get_event_loop()
                xx = await loop.run_in_executor(None, download, url, my_hook)
                file = await convert(xx)
                await music.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            file,
                        ),
                    ),
                )
                thumbnail = x["thumbnail"]
                duration = x["duration"]
                duration = round(x["duration"] / 60)
                theme = random.choice(themes)
                ctitle = (await app.get_chat(chat_id)).title
                ctitle = await CHAT_TITLE(ctitle)
                f2 = open(f"search/{afk}id.txt", "r")
                userid = f2.read()
                thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                user_id = userid
                buttons = play_markup(videoid, user_id)
                await mystic.delete()
                semx = await app.get_users(userid)
                user_id = CallbackQuery.from_user.id
                user_name = CallbackQuery.from_user.first_name
                rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
                await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"""
<b>⏭️ Melewati lagu permintaa {rpk}</b>

<b>🏷 Nama: </b>[{title[:25]}]({url})
<b>⏱️ Durasi: :</b> {duration}
<b>🎧 Atas permintaan:</b> {semx.mention}
"""
                    ),
                )
                os.remove(thumb)
            else:
                await music.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            afk,
                        ),
                    ),
                )
                _chat_ = (
                    (str(afk))
                    .replace("_", "", 1)
                    .replace("/", "", 1)
                    .replace(".", "", 1)
                )
                f2 = open(f"search/{_chat_}title.txt", "r")
                title = f2.read()
                f3 = open(f"search/{_chat_}duration.txt", "r")
                duration = f3.read()
                f4 = open(f"search/{_chat_}username.txt", "r")
                username = f4.read()
                f4 = open(f"search/{_chat_}videoid.txt", "r")
                videoid = f4.read()
                user_id = 1
                videoid = str(videoid)
                if videoid == "smex1":
                    buttons = audio_markup(videoid, user_id)
                else:
                    buttons = play_markup(videoid, user_id)
                user_id = CallbackQuery.from_user.id
                user_name = CallbackQuery.from_user.first_name
                rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
                await CallbackQuery.message.reply_photo(
                    photo=f"downloads/{_chat_}final.png",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"""
<b>⏭️ Melewati lagu permintaa: {rpk}</b>

<b>🏷️ Nama:</b> {title}
<b>⌚ Durasi</b> {duration}
<b>🎧 Atas permintaan:</b> {username}
""",
                )
                return


@Client.on_callback_query(filters.regex("stopvc"))
async def stopvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "You don't have the required permission to perform this action.\nPermission: MANAGE VOICE CHATS",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        try:
            await music.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Dihentikan", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.message.reply(f"🎧 Lagu Dihentikan oleh {rpk}!")
    else:
        await CallbackQuery.answer(f"Tidak ada yang diputar!", show_alert=True)
