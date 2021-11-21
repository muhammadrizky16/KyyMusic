import yt_dlp
from Music import ASSID, BOT_ID, BOT_NAME, BOT_USERNAME, OWNER, SUDOERS, app
from Music.MusicUtilities.database.chats import is_served_chat
from Music.MusicUtilities.database.queue import remove_active_chat
from Music.MusicUtilities.database.sudo import get_sudoers
from Music.MusicUtilities.helpers.inline import personal_markup
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton(
                text="📚 Daftar Perintah 📚",
                url="https://telegra.ph/ᴷʸʸ-11-21-2",
            )
        ],
    ]
    return (
        "🎛 **{BOT_NAME} Merupakan salah satu dari bot telegram yang bisa memutar musik di grup**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ Tambahkan Saya Ke Grup ➕",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                "📚 Perintah", url="https://telegra.ph/ᴷʸʸ-11-21-2"
            )
        ],
    ]
)
welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(chat_id):
        await message.reply_text(
            f"""
**Grup ini belum dapat ijin.**

Untuk mendapatkan ijin menggunakan bot.
Silahkan Pm Daftar Admin Saya [Dari Sini](https://t.me/{BOT_USERNAME}?start=sudolist)
"""
        )
        return await app.leave_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(
                    f"💡 Pemilik Bot [{member.mention}] baru saja bergabung di grup ini."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"💡 Admin Bot [{member.mention}] baru saja bergabung di grup ini."
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
👋 ** Halo senang rasanya bisa bergabung di grup ini**

💡 **Jangan lupa untuk menjadikan saya sebagai admin di grup ini**
""",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                )
                return
        except BaseException:
            return


@Client.on_message(
    filters.group
    & filters.command(
        ["start", "help", f"start@{BOT_USERNAME}", f"help@{BOT_USERNAME}"]
    )
)
async def start(_, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(chat_id):
        await message.reply_text(
            f"""
**Grup ini belum dapat ijin.**

Untuk mendapatkan ijin menggunakan bot.
Silahkan Pm Daftar Admin Saya [Dari Sini](https://t.me/{BOT_USERNAME}?start=sudolist)
"""
        )
        return await app.leave_chat(chat_id)
    out = start_pannel()
    await message.reply_text(
        f"""
Terima kasih telah memasukkan saya di {message.chat.title}.
Musik itu hidup.

Untuk bantuan silahkan klik tombol dibawah.
""",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )
    return


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await app.send_message(
            message.chat.id,
            text=f"""
**✨ Selamat Datang {rpk}!

💬 [{BOT_NAME}](t.me/{BOT_USERNAME}) memungkinkan anda untuk memutar musik pada grup melalui obrolan suara yang baru di Telegram!

💡 Untuk Mengetahui Semua Perintah Bot Dan Bagaimana Cara Kerja Nya Dengan Menekan Tombol » 📚 Perintah!

✅ Jika Anda Menginginkan Saya Bergabung Di Grup Anda Silahkan Kirim ID Grup Telegram Anda Kepada Admin [cek daftar admin](https://t.me/{BOT_USERNAME}?start=sudolist)**
""",
            parse_mode="markdown",
            reply_markup=pstart_markup,
            reply_to_message_id=message.message_id,
        )
    elif len(message.command) == 2:
        query = message.text.split(None, 1)[1]
        f1 = query[0]
        f2 = query[1]
        f3 = query[2]
        finxx = f"{f1}{f2}{f3}"
        if str(finxx) == "inf":
            query = (str(query)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = x["thumbnail"]
            searched_text = f"""
🔍 **Video Track Information**

❇️**Judul:** {x["title"]}

⏳ **Durasi:** {round(x["duration"] / 60)} Mins
👀 **Ditonton:** `{x["view_count"]}`
👍 **Suka:** `{x["like_count"]}`
👎 **Tidak suka:** `{x["dislike_count"]}`
⭐️ **Peringkat Rata-rata:** {x["average_rating"]}
🎥 **Nama channel:** {x["uploader"]}
📎 **Channel Link:** [Kunjungi Dari Sini]({x["channel_url"]})
🔗 **Link:** [Link]({x["webpage_url"]})
"""
            link = x["webpage_url"]
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(
                message.chat.id,
                photo=thumb,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**📝 DAFTAR PENGGUNA SUDO**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue
                text += f"- {user}\n"
            if not text:
                await message.reply_text("Tidak Ada Pengguna Sudo")
            else:
                await message.reply_text(text)
