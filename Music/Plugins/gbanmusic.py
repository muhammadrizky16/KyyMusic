import asyncio

from Music import BOT_ID, OWNER, app
from Music.MusicUtilities.database.chats import get_served_chats
from Music.MusicUtilities.database.gbanned import (
    add_gban_user,
    is_gbanned_user,
    remove_gban_user,
)
from Music.MusicUtilities.database.sudo import get_sudoers
from pyrogram import filters
from pyrogram.errors import FloodWait


@app.on_message(filters.command("gban") & filters.user(OWNER))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**Penggunaan:**\n/block [USERNAME | USER_ID]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            return await message.reply_text("Anda ingin memblokir diri sendiri?")
        elif user.id == BOT_ID:
            await message.reply_text("Haruskah saya memblokir diri saya sendiri??")
        elif user.id in sudoers:
            await message.reply_text("Anda ingin memblokir pengguna sudo?")
        else:

            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"""
**Menginisialisasi Larangan Global pada {user.mention}**

Waktu yang diharapkan: {len(served_chats)}
"""
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Larangan Global Baru pada Musik**__
**Asal:** {message.chat.title} [`{message.chat.id}`]
**Pengguna Sudo:** {from_user.mention}
**Pengguna yang Diblokir:** {user.mention}
**ID Pengguna yang diblokir:** `{user.id}`
**Obrolan:** {number_of_chats}
"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Anda ingin memblokir diri sendiri?")
    elif user_id == BOT_ID:
        await message.reply_text("Haruskah saya memblokir diri saya sendiri??")
    elif user_id in sudoers:
        await message.reply_text("Anda ingin memblokir pengguna sudo?")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("Sudah Gbanned.")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"""
**Menginisialisasi Larangan Global pada {mention}**

Waktu yang diharapkan: {len(served_chats)}
"""
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Larangan Global Baru pada Musik**__
**Asal:** {message.chat.title} [`{message.chat.id}`]
**Pengguna Sudo:** {from_user_mention}
**Pengguna yang Diblokir:** {mention}
**ID Pengguna yang obrolan:** `{user_id}`
**Obrolan:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(OWNER))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("**Penggunaan:**\n/unblock [USERNAME | USER_ID]")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("Anda ingin membuka blokir diri sendiri?")
        elif user.id == BOT_ID:
            await message.reply_text("Haruskah saya membuka blokir sendiri??")
        elif user.id in sudoers:
            await message.reply_text("Pengguna Sudo tidak dapat diblokir/diblokir.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("Dia sudah bebas, mengapa menggertaknya?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"Ungbanned!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Anda ingin membuka blokir diri sendiri?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Haruskah saya membuka blokir sendiri? Tapi saya tidak diblokir."
        )
    elif user_id in sudoers:
        await message.reply_text("Pengguna Sudo tidak dapat diblokir/diblokir.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("Dia sudah bebas, mengapa menggertaknya?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"Ungbanned!")


chat_watcher_group = 5


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.kick_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"""
{checking} secara global dilarang oleh Musik dan telah dikeluarkan dari obrolan.

**Kemungkinan Alasan:** Potensi Spammer dan Penyalahguna.
"""
        )
