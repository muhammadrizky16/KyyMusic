import os

import yt_dlp
from Music import BOT_NAME, BOT_USERNAME, app
from Music.config import DURATION_LIMIT
from Music.MusicUtilities.database.chats import is_served_chat
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.gets import get_url
from Music.MusicUtilities.helpers.inline import search_markup
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython import VideosSearch

flex = {}
chat_watcher_group = 3


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


@Client.on_message(
    command(["song", f"song@{BOT_USERNAME}", "vsong", f"vsong@{BOT_USERNAME}"])
)
async def mpthree(_, message: Message):
    chat_id = message.chat.id
    if message.sender_chat:
        return await message.reply_text(
            """
Anda adalah Admin Anonim!
Kembalikan ke Akun Pengguna Dari Hak Admin.
"""
        )
    user_id = message.from_user.id
    message.chat.title
    message.from_user.first_name
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    url = get_url(message)
    if url:
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("Sedang memproses")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"]
                (result["link"])
                (result["id"])
                videoid = result["id"]
        except Exception as e:
            return await mystic.edit_text(f"Soung Not Found.\n**Possible Reason:**{e}")
        smex = int(time_to_seconds(duration))
        if smex > DURATION_LIMIT:
            return await mystic.edit_text(
                f"**__Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)"
            )
        if duration == "None":
            return await mystic.edit_text("Sorry! Live videos are not Supported")
        if views == "None":
            return await mystic.edit_text("Sorry! Live videos are not Supported")
        thumb = await down_thumb(thumbnail, user_id)
        buttons = gets(videoid, user_id)
        m = await message.reply_text(
            f"""
<b>🏷️ Judul:</b> [{title[:25]}]({url})
<b>💡</b> [More Information](https://t.me/{BOT_USERNAME}?start=info_{id})
<b>⚡ Didukung</b> [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        os.remove(thumb)
    else:
        if len(message.command) < 2:
            await message.reply_text(
                """
**Penggunaan:**

/song atau /vsong [Judul Lagu Atau Youtube Link] - untuk mendownload lagu dan video
"""
            )
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("**🔎 Pencarian**")
        try:
            a = VideosSearch(query, limit=5)
            result = (a.result()).get("result")
            title1 = result[0]["title"]
            duration1 = result[0]["duration"]
            title2 = result[1]["title"]
            duration2 = result[1]["duration"]
            title3 = result[2]["title"]
            duration3 = result[2]["duration"]
            title4 = result[3]["title"]
            duration4 = result[3]["duration"]
            title5 = result[4]["title"]
            duration5 = result[4]["duration"]
            ID1 = result[0]["id"]
            ID2 = result[1]["id"]
            ID3 = result[2]["id"]
            ID4 = result[3]["id"]
            ID5 = result[4]["id"]
        except Exception as e:
            return await mystic.edit_text(
                f"Lagu Tidak Ditemukan.\\in**Kemungkinan Alasan:** {e}"
            )
        await mystic.delete()
        buttons = search_markup(
            ID1,
            ID2,
            ID3,
            ID4,
            ID5,
            duration1,
            duration2,
            duration3,
            duration4,
            duration5,
            user_id,
            query,
        )
        hmo = await message.reply_text(
            f"**✨ Silahkan Pilih Mana Yang Ingin Didownload**\n\n¹ <b>{title1[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n² <b>{title2[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n³ <b>{title3[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n⁴ <b>{title4[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n⁵ <b>{title5[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )  
        return


@Client.on_callback_query(filters.regex(pattern=r"beta"))
async def startyuplay(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    CallbackQuery.message.chat.id
    CallbackQuery.message.chat.title
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    try:
        id, duration, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"Error Occured\n**Possible reason could be**:{e}"
        )
    if duration == "None":
        return await CallbackQuery.message.reply_text(
            f"Sorry!, Live Videos are not supported"
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "This is not for you! Search You Own Song nigga", show_alert=True
        )
    await CallbackQuery.message.delete()
    checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    url = f"https://www.youtube.com/watch?v={id}"
    videoid = id
    smex = int(time_to_seconds(duration))
    if smex > DURATION_LIMIT:
        await CallbackQuery.message.reply_text(
            f"**__Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)"
        )
        return
    try:
        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
            x = ytdl.extract_info(url, download=False)
    except Exception as e:
        return await CallbackQuery.message.reply_text(
            f"Failed to download this video.\n\n**Reason**:{e}"
        )
    title = x["title"]
    await CallbackQuery.answer(
        f"Selected {title[:20]}.... \nProcessing..", show_alert=True
    )
    thumbnail = x["thumbnail"]
    (x["id"])
    videoid = x["id"]
    thumb = await down_thumb(thumbnail, user_id)
    buttons = gets(videoid, user_id)
    m = await CallbackQuery.message.reply_photo(
        photo=thumb,
        reply_markup=InlineKeyboardMarkup(buttons),
        caption=f"""
<b>🏷️ Judul:</b> [{title[:25]}]({url})
├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{id})
└ ⚡ **Didukung:** [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
    )
    os.remove(thumb)
    await CallbackQuery.message.delete()


@Client.on_callback_query(filters.regex(pattern=r"chonga"))
async def chonga(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    print(callback_request)
    CallbackQuery.from_user.id
    try:
        id, query, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"Error Occured\n**Possible reason could be**:{e}"
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "This is not for you! Search You Own Song", show_alert=True
        )
    i = int(id)
    query = str(query)
    try:
        a = VideosSearch(query, limit=10)
        result = (a.result()).get("result")
        title1 = result[0]["title"]
        duration1 = result[0]["duration"]
        title2 = result[1]["title"]
        duration2 = result[1]["duration"]
        title3 = result[2]["title"]
        duration3 = result[2]["duration"]
        title4 = result[3]["title"]
        duration4 = result[3]["duration"]
        title5 = result[4]["title"]
        duration5 = result[4]["duration"]
        title6 = result[5]["title"]
        duration6 = result[5]["duration"]
        title7 = result[6]["title"]
        duration7 = result[6]["duration"]
        title8 = result[7]["title"]
        duration8 = result[7]["duration"]
        title9 = result[8]["title"]
        duration9 = result[8]["duration"]
        title10 = result[9]["title"]
        duration10 = result[9]["duration"]
        ID1 = result[0]["id"]
        ID2 = result[1]["id"]
        ID3 = result[2]["id"]
        ID4 = result[3]["id"]
        ID5 = result[4]["id"]
        ID6 = result[5]["id"]
        ID7 = result[6]["id"]
        ID8 = result[7]["id"]
        ID9 = result[8]["id"]
        ID10 = result[9]["id"]
    except Exception as e:
        return await mystic.edit_text(
            f"Lagu Tidak Ditemukan.\\in**Kemungkinan Alasan:** {e}"
        )
    if i == 1:
        buttons = search_markup2(
            ID6,
            ID7,
            ID8,
            ID9,
            ID10,
            duration6,
            duration7,
            duration8,
            duration9,
            duration10,
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"**✨ Silahkan Pilih Mana Yang Ingin Didownload**⁶ <b>{title6[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID6})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n⁷ <b>{title7[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID7})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n⁸ <b>{title8[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID8})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n⁹ <b>{title9[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID9})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n¹⁰ <b>{title10[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID10})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )  
        return
    if i == 2:
        buttons = search_markup(
            ID1,
            ID2,
            ID3,
            ID4,
            ID5,
            duration1,
            duration2,
            duration3,
            duration4,
            duration5,
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"**✨ Silahkan Pilih Mana Yang Ingin Didownload**¹ <b>{title1[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n² <b>{title2[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n³ <b>{title3[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n⁴ <b>{title4[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>\n\n⁵ <b>{title5[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})__</u>\n  ┗ ⚡ <u>__Powered by {BOT_NAME}__</u>",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True 
        )  
        return

def search_markup(
    ID1,
    ID2,
    ID3,
    ID4,
    ID5,
    duration1,
    duration2,
    duration3,
    duration4,
    duration5,
    user_id,
    query,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="¹", callback_data=f"beta {ID1}|{duration1}|{user_id}"
            ),
            InlineKeyboardButton(
                text="²", callback_data=f"beta {ID2}|{duration2}|{user_id}"
            ),
            InlineKeyboardButton(
                text="³", callback_data=f"beta {ID3}|{duration3}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⁴", callback_data=f"beta {ID4}|{duration4}|{user_id}"
            ),
            InlineKeyboardButton(
                text="⁵", callback_data=f"beta {ID5}|{duration5}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⪻", callback_data=f"chonga 1|{query}|{user_id}"
            ),
            InlineKeyboardButton(text="✘", callback_data=f"ppcl2 smex|{user_id}"),
            InlineKeyboardButton(
                text="⪼", callback_data=f"chonga 1|{query}|{user_id}"
            ),
        ],
    ]
    return buttons


def search_markup2(
    ID6,
    ID7,
    ID8,
    ID9,
    ID10,
    duration6,
    duration7,
    duration8,
    duration9,
    duration10,
    user_id,
    query,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="⁶", callback_data=f"beta {ID6}|{duration6}|{user_id}"
            ),
            InlineKeyboardButton(
                text="⁷", callback_data=f"beta {ID7}|{duration7}|{user_id}"
            ),
            InlineKeyboardButton(
                text="⁸", callback_data=f"beta {ID8}|{duration8}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⁹", callback_data=f"beta {ID9}|{duration9}|{user_id}"
            ),
            InlineKeyboardButton(
                text="¹⁰", callback_data=f"beta {ID10}|{duration10}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⪻", callback_data=f"chonga 2|{query}|{user_id}"
            ),
            InlineKeyboardButton(text="✘", callback_data=f"ppcl2 smex|{user_id}"),
            InlineKeyboardButton(
                text="⪼", callback_data=f"chonga 2|{query}|{user_id}"
            ),
        ],
    ]
    return buttons


def gets(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴀᴜᴅɪᴏ", callback_data=f"gets audio|{videoid}|{user_id}"
            ),
            InlineKeyboardButton(
                text="ᴠɪᴅᴇᴏ", callback_data=f"gets video|{videoid}|{user_id}"
            ),
        ],
        [InlineKeyboardButton(text="ᴛᴜᴛᴜᴘ", callback_data=f"close2")],
    ]
    return buttons
