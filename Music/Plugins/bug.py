from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Music import BOT_USERNAME, SUDOERS, app
from Music.config import LOG_GROUP_ID, OWNER_USERNAME
from Music.MusicUtilities.helpers.filters import command


def get_text(message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None



@app.on_message(command(["bug", f"bug@{BOT_USERNAME}"]) & filters.group)
async def bug(_, message):
    report = get_text(message)
    if message.chat.username:
        chatusername = f"[{message.chat.title}](t.me/{message.chat.username})"
    else:
        chatusername = f"{message.chat.title}"
    if not report:
        await message.reply(
            "Contoh menggunakan fitur ini\n`/bug assisten nggak mau turun`",
        )
        return
    await app.send_message(
        LOG_GROUP_ID,
        f"""
**✅ {OWNER_USERNAME} Tuan Ada Laporan Baru

🧑‍💼 Pengguna: {message.from_user.mention}
💡 Group: {chatusername}
🆔 ID: `{message.chat.id}`

💬 Pesan: {report}**
""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"• {message.from_user.first_name} •",
                        url=f"{message.link}",
                    )
                ]
            ]
        ),
    )
    await message.reply(
        f"**🙏🏻 Terimakasih {message.from_user.mention} laporan anda telah terkirim ke admin**"
    )


@app.on_message(command(["send", f"send@{BOT_USERNAME}"]) & filters.user(SUDOERS))
async def send(_, message):
    text = get_text(message)
    texting = message.reply_to_message
    await app.send_message(text, texting.text)


@app.on_message(command(["rsend", f"rsend@{BOT_USERNAME}"]) & filters.user(SUDOERS))
async def rsend(_, message):
    text = get_text(message)
    stickers = message.reply_to_message
    await app.send_sticker(text, stickers.sticker.file_id)
