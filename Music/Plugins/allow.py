from Music import SUDOERS, app
from Music.MusicUtilities.database.chats import (
    add_served_chat,
    get_served_chats,
    is_served_chat,
    remove_served_chat,
)
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command("addchat") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            """
**Penggunaan:**
/addchat [CHAT_ID]
"""
        )
    chat_id = int(message.text.strip().split()[1])
    if not await is_served_chat(chat_id):
        await add_served_chat(chat_id)
        await message.reply_text("TAMBAHKAN CHAT KE DAFTAR YANG DIIZINKAN")
    else:
        await message.reply_text("SUDAH DALAM DAFTAR YANG DIPERBOLEHKAN")


@app.on_message(filters.command("unchat") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            """
**Penggunaan:**
/unchat [CHAT_ID]
"""
        )
    chat_id = int(message.text.strip().split()[1])
    if not await is_served_chat(chat_id):
        await message.reply_text("Obrolan tidak diizinkan.")
        return
    try:
        await remove_served_chat(chat_id)
        await message.reply_text("Obrolan tidak diizinkan.")
        return
    except Exception:
        await message.reply_text("Error.")


@app.on_message(filters.command("add") & filters.user(SUDOERS))
async def blacklisted_chats_func(_, message: Message):
    served_chats = []
    text = "**Obrolan yang Diizinkan**\n"
    try:
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception:
        await message.reply_text("Error.")
        return
    count = 0
    for served_chat in served_chats:

        try:
            title = (await app.get_chat(served_chat)).title
        except Exception:
            title = "Private"
        count += 1
        text += f"**{count}. {title}** [`{served_chat}`]\n"
    if not text:
        await message.reply_text("Tidak ada Obrolan yang Diizinkan")
    else:
        await message.reply_text(text)
