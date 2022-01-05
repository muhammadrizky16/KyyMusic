import asyncio
import os
import random
from asyncio import QueueEmpty
from Music.config import GROUP, CHANNEL
from Music import BOT_NAME, BOT_USERNAME, app
from Music.MusicUtilities.database.queue import is_active_chat, remove_active_chat
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.gets import get_url, themes
from Music.MusicUtilities.helpers.logger import LOG_CHAT
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.tgcallsrun import ASS_ACC, clear, music
from Music.MusicUtilities.tgcallsrun.queues import QUEUE, add_to_queue, clear_queue
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def clear_queue(chat_id):
    if chat_id in QUEUE:
        QUEUE.pop(chat_id)
        return 1
    else:
        return 0


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                title = r["title"][:70]
            else:
                title = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
            duration = r["duration"]
            videoid = r["id"]
        return [title, url, duration, videoid]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()
    

@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & filters.group)
async def vplay(c: Client, message: Message):
    replied = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP}"),
                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/{CHANNEL}"),
            ]
        ]
    )
    if message.sender_chat:
        return await message.reply_text(
            "Anda adalah **Admin Anonim!**\n\n» kembali ke akun pengguna dari hak admin."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await message.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await message.reply_text(
            f"""
💡 Untuk menggunakan saya, Saya perlu menjadi admin dengan izin:

» ❌ Hapus pesan
» ❌ Blokir pengguna
» ❌ Tambah pengguna
» ❌ Kelola obrolan suara

✨ Powered by: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_manage_voice_chats:
        await message.reply_text(
            f"""
💡 Untuk menggunakan saya, Saya perlu menjadi admin dengan izin:

» ❌ Kelola obrolan suara

✨ Powered by: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_delete_messages:
        await message.reply_text(
            f"""
💡 Untuk menggunakan saya, Saya perlu menjadi admin dengan izin:

» ❌ Hapus pesan

✨ Powered by: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_invite_users:
        await message.reply_text(
            f"""
💡 Untuk menggunakan saya, Saya perlu menjadi admin dengan izin:

» ❌ Tambah pengguna

✨ Powered by: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    try:
        ubot = await ASS_ACC.get_me()
        b = await app.get_chat_member(message.chat.id, ubot.id)
        if b.status == "kicked":
            await app.unban_chat_member(message.chat.id, ubot.id)
            invite_link = await app.export_chat_invite_link(message.chat.id)
            if "+" in invite_link:
                invite = (invite_link.replace("+", "")).split("t.me/")[1]
                link_invite = f"https://t.me/joinchat/{invite}"
            await ASS_ACC.join_chat(link_invite)
            await app.send_message(
                message.chat.id,
                f"{ubot.first_name} Berhasil Bergabung",
            )
    except UserNotParticipant:
        try:
            invite_link = await app.export_chat_invite_link(message.chat.id)
            if "+" in invite_link:
                invite = (invite_link.replace("+", "")).split("t.me/")[1]
                link_invite = f"https://t.me/joinchat/{invite}"
            await ASS_ACC.join_chat(link_invite)
            await app.send_message(
                message.chat.id,
                f"{ubot.first_name} Berhasil Bergabung",
            )
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await message.reply_text(
                f"❌ **@{ubot.username} Assistant gagal bergabung**\n\n**Alasan**: `{e}`"
            )

    replied = message.reply_to_message
    url = get_url(message)
    if replied:
        if replied.video or replied.document:
            what = "Video or Document Format"
            await LOG_CHAT(message, what)
            loser = await replied.reply("📥 **Mengunduh Video...**")
            dl = await replied.download()
            link = replied.link
            if len(message.command) < 2:
                Q = 720
            else:
                pq = message.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» **Hanya 720, 480, 360 Yang Diizinkan** \n💡 **Sekarang Streaming Video Di 720p**"
                    )
            try:
                if replied.video:
                    title = replied.video.file_name[:70]
                    duration = replied.video.duration
                elif replied.document:
                    title = replied.document.file_name[:70]
                    duration = replied.document.duration
            except BaseException:
                pass
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, title, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                await app.send_message(
                    chat_id,
                    f"""
💡 **Trek ditambahkan ke antrian**

🏷 **Judul:** [{title[:999]}]({link})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}

#️⃣ **Posisi antrian** {pos}
""",
                    disable_web_page_preview=True,
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                if await is_active_chat(chat_id):
                    try:
                        clear(chat_id)
                    except QueueEmpty:
                        pass
                    await remove_active_chat(chat_id)
                    await music.pytgcalls.leave_group_call(chat_id)
                await music.pytgcalls.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, title, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                await app.send_message(
                    chat_id,
                    f"""
▷ **Memutar video dimulai**

🏷 **Judul:** [{title[:999]}]({link})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}

💬 **Diputar di:** {message.chat.title}
""",
                    disable_web_page_preview=True,
                    reply_markup=keyboard,
                )

    elif url:
        what = "URL vplay"
        await LOG_CHAT(message, what)
        query = message.text.split(None, 1)[1]
        kz = await message.reply_text("** Memproses url...**")
        try:
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                thumbnail = f"https://i.ytimg.com/vi/{result['id']}/hqdefault.jpg"
                url = result["link"]
                (result["id"])
                result["id"]
        except Exception as e:
            return await kz.edit_text(
                f"Lagu Tidak Ditemukan.\n**Kemungkinan Alasan:** {e}"
            )
        Q = 360
        amaze = HighQualityVideo()
        theme = random.choice(themes)
        srrf = message.chat.title
        ctitle = await CHAT_TITLE(srrf)
        userid = message.from_user.id
        thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
        z, ytlink = await ytdl(url)
        if z == 0:
            await CallbackQuery.message.reply_text(
                f"❌ yt-dl masalah terdeteksi\n\n» `{ytlink}`"
            )
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, title, ytlink, url, "Video", Q)
                requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                await app.send_photo(
                    chat_id,
                    photo=thumb,
                    caption=f"""
💡 **Trek ditambahkan ke antrian**

🏷 **Judul:** [{title[:999]}]({url})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}

#️⃣ **Posisi antrian** {pos}
""",
                    reply_markup=keyboard,
                )
            else:
                try:
                    if await is_active_chat(chat_id):
                        try:
                            clear(chat_id)
                        except QueueEmpty:
                            pass
                        await remove_active_chat(chat_id)
                        await music.pytgcalls.leave_group_call(chat_id)
                    await music.pytgcalls.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            ytlink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, title, ytlink, url, "Video", Q)
                    await kz.delete()
                    requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                    await app.send_photo(
                        chat_id,
                        photo=thumb,
                        caption=f"""
▷ **Memutar video dimulai**

🏷 **Judul:** [{title[:999]}]({url})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}

💬 **Diputar di:** {message.chat.title}
""",
                        reply_markup=keyboard,
                    )
                except Exception as e:
                    await message.reply_text(f"Error: `{e}`")

    else:
        if len(message.command) < 2:
            await message.reply_text(
                text=f"""
**{rpk} Anda tidak memberikan judul.

Coba berikan judul atau url untuk diputar!**
» `/vplay duka`""",
            )
        else:
            what = "Command vplay"
            await LOG_CHAT(message, what)
            loser = await message.reply("**🔎 Pencarian...**")
            query = message.text.split(None, 1)[1]
            Q = 360
            amaze = LowQualityVideo()
            try:
                result = VideosSearch(query, limit=5).result()
                data = result["result"]
            except BaseException:
                await loser.edit("**Anda tidak memberikan judul lagu apapun !**")
            # kontol kalian
            try:
                toxxt = f"**✨ Silahkan pilih video yang ingin anda putar**\n\n"
                j = 0

                emojilist = [
                    "¹",
                    "²",
                    "³",
                    "⁴",
                    "⁵",
                ]
                while j < 5:
                    toxxt += f"{emojilist[j]} **[{data[j]['title'][:25]}...]({data[j]['link']})**\n"
                    toxxt += f"⏱ **Durasi:** {data[j]['duration']}\n"
                    toxxt += f"💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{data[j]['id']})\n"
                    toxxt += f"⚡ **Powered by:** {BOT_NAME}\n\n"
                    j += 1
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "¹", callback_data=f"plll 0|{query}|{user_id}"
                            ),
                            InlineKeyboardButton(
                                "²", callback_data=f"plll 1|{query}|{user_id}"
                            ),
                            InlineKeyboardButton(
                                "³", callback_data=f"plll 2|{query}|{user_id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "⁴", callback_data=f"plll 3|{query}|{user_id}"
                            ),
                            InlineKeyboardButton(
                                "⁵", callback_data=f"plll 4|{query}|{user_id}"
                            ),
                        ],
                        [InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="cls")],
                    ]
                )
                await message.reply(toxxt, disable_web_page_preview=True, reply_markup=key)

                await loser.delete()
                # kontol
                return
                # kontol
            except Exception as e:
                await loser.edit(f"**❌ Error:** `{e}`")
                return
            try:
                songname = data["title"]
                url = data["link"]
                duration = data["duration"]
                thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
                data["id"]
            except BaseException:
                await loser.edit(
                    "**❌ Video tidak ditemukan.** berikan judul video yang valid."
                )
            theme = random.choice(themes)
            srrf = message.chat.title
            ctitle = await CHAT_TITLE(srrf)
            userid = message.from_user.id
            thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
            ytlink = await ytdl(url)
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                await loser.delete()
                requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                await app.send_photo(
                    chat_id,
                    photo=thumb,
                    caption=f"""
💡 **Trek ditambahkan ke antrian**

🏷 **Judul:** [{songname[:999]}]({url})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}

#️⃣ **Posisi antrian** {pos}
""",
                    reply_markup=keyboard,
                )
            else:
                try:
                    if await is_active_chat(chat_id):
                        try:
                            clear(chat_id)
                        except QueueEmpty:
                            pass
                        await remove_active_chat(chat_id)
                        await music.pytgcalls.leave_group_call(chat_id)
                    await music.pytgcalls.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            ytlink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, title, ytlink, url, "Video", Q)
                    await loser.delete()
                    requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                    await message.reply_photo(
                        chat_id,
                        photo=thumb,
                        caption=f"""
▷ **Memutar video dimulai**

🏷 **Judul:** [{songname[:999]}]({url})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}

💬 **Diputar di:** {message.chat.title}
""",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await loser.delete()
                    await message.reply_text(f"Error: `{ep}`")


@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def kontol(_, CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP}"),
                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/{CHANNEL}"),
            ]
        ]
    )
    chat_id = CallbackQuery.message.chat.id
    userid = CallbackQuery.from_user.id
    callback_data = CallbackQuery.data.strip()
    CallbackQuery.message.chat.title
    callback_request = callback_data.split(None, 1)[1]
    try:
        x, query, user_id = callback_request.split("|")
    except Exception as e:
        await CallbackQuery.message.reply_text(f"âŒ **Error:** `{e}`")
        return
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Ini bukan untukmu! Cari Video Anda Sendiri", show_alert=True
        )
    await CallbackQuery.message.delete()
    requester = f"[{CallbackQuery.from_user.first_name}](tg://user?id={CallbackQuery.from_user.id})"
    x = int(x)
    Q = 360
    amaze = HighQualityVideo()
    a = VideosSearch(query, limit=5)
    data = (a.result()).get("result")
    songname = data[x]["title"]
    title = data[x]["title"]
    data[x]["id"]
    duration = data[x]["duration"]
    url = f"https://www.youtube.com/watch?v={data[x]['id']}"
    thumbnail = f"https://i.ytimg.com/vi/{data[x]['id']}/hqdefault.jpg"
    theme = random.choice(themes)
    srrf = CallbackQuery.message.chat.title
    ctitle = await CHAT_TITLE(srrf)
    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
    kz, ytlink = await ytdl(url)
    if kz == 0:
        await CallbackQuery.message.reply_text(
            f"❌ yt-dl masalah terdeteksi\n\n» `{ytlink}`"
        )
    else:
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
            await app.send_photo(
                chat_id,
                photo=thumb,
                caption=f"""
💡 **Trek ditambahkan ke antrian**

🏷 **Judul:** [{songname[:999]}]({url})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}

#️⃣ **Posisi antrian** {pos}
""",
                reply_markup=keyboard,
            )
            os.remove(thumb)
            await CallbackQuery.message.delete()
        else:
            try:
                if await is_active_chat(chat_id):
                    try:
                        clear(chat_id)
                    except QueueEmpty:
                        pass
                    await remove_active_chat(chat_id)
                    await music.pytgcalls.leave_group_call(chat_id)
                await music.pytgcalls.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        ytlink,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                await app.send_photo(
                    chat_id,
                    photo=thumb,
                    caption=f"""
▷ **Memutar video dimulai**

🏷 **Judul:** [{songname[:999]}]({url})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}

💬 **Diputar di:** {CallbackQuery.message.chat.title}
""",
                    reply_markup=keyboard,
                )
            except Exception as e:
                os.remove(thumb)
                await CallbackQuery.message.reply_text(f"**Error:** `{e}`")
