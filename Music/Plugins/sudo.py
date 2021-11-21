import os

from Music import OWNER, app
from Music.MusicUtilities.database.sudo import add_sudo, get_sudoers, remove_sudo
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command("addsudo") & filters.user(OWNER))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Balas pesan pengguna atau berikan nama pengguna/id_pengguna."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        message.from_user
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("Sudah menjadi Pengguna Sudo.")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"Ditambahkan **{user.mention}** Sebagai Pengguna sudo"
            )
            return os.execvp("python3", ["python3", "-m", "Music"])
        await edit_or_reply(message, text="Terjadi kesalahan, periksa log.")
        return
    message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await message.reply_text("Sudah menjadi Pengguna Sudo.")
    added = await add_sudo(user_id)
    if added:
        await message.reply_text(f"Ditambahkan **{mention}** Sebagai Pengguna Sudo")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await edit_or_reply(message, text="Terjadi kesalahan, periksa log.")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Membalas pesan pengguna atau memberikan nama pengguna/id_pengguna."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        message.from_user
        if user.id not in await get_sudoers():
            return await message.reply_text(f"Not a part of Music's Sudo.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"Menghapus **{user.mention}** dari Sudo.")
            return os.execvp("python3", ["python3", "-m", "Music"])
        await message.reply_text(f"Sesuatu yang salah terjadi.")
        return
    message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in await get_sudoers():
        return await message.reply_text(f"Bukan bagian dari Sudo Musik.")
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(f"Menghapus **{mention}** dari Sudo.")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await message.reply_text(f"Something wrong happened.")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "**Daftar Pengguna Sudo**\n\n"
    for count, user_id in enumerate(sudoers, 1):
        try:
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
        except Exception:
            continue
        text += f"• {user}\n"
    if not text:
        await message.reply_text("Tidak Ada Pengguna Sudo")
    else:
        await message.reply_text(text)
