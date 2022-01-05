import asyncio

from Music import BOT_USERNAME, SUDOERS
from Music import client as USER
from Music.MusicUtilities.helpers.filters import command
from pyrogram import Client, filters


@Client.on_message(
    command(["userbotleaveall", f"userbotleaveall@{BOT_USERNAME}"])
    & filters.user(SUDOERS)
    & ~filters.edited
)
async def bye(client, message):
    if message.from_user.id in SUDOERS:
        left = 0
        failed = 0
        lol = await message.reply("Asisten Meninggalkan semua obrolan")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"""
**🔄 Sedang Memproses**

**✅ Keluar: {left}**
**❌ Gagal: {failed}**
"""
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"""
**🔄 Sedang Memproses**

**✅ Keluar: {left}**
**❌ Gagal: {failed}**
"""
                )
            await asyncio.sleep(10)
        await lol.delete()
        await client.send_message(
            message.chat.id,
            f"""
**💡 Assistant Telah Keluar**

**✅ Keluar: {left}**
**❌ Gagal: {failed}**
""",
        )
