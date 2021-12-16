from pyrogram.raw.base import Update
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from pytgcalls.types.stream import StreamVideoEnded

from Music import app
from Music.config import GROUP, CHANNEL, call_py
from Music.MusicUtilities.tgcallsrun.queues import (
    QUEUE,
    clear_queue,
    get_queue,
    pop_an_item,
)

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("ᴅᴏɴᴀsɪ", url="https://t.me/{GROUP}"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/{CHANNEL}"),
        ]
    ]
)


async def skip_current_song(chat_id):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            try:
                songname = chat_queue[1][0]
                url = chat_queue[1][1]
                link = chat_queue[1][2]
                type = chat_queue[1][3]
                Q = chat_queue[1][4]
                if type == "Audio":
                    await call_py.change_stream(
                        chat_id,
                        AudioPiped(
                            url,
                        ),
                    )
                elif type == "Video":
                    if Q == 720:
                        hm = HighQualityVideo()
                    elif Q == 480:
                        hm = MediumQualityVideo()
                    elif Q == 360:
                        hm = LowQualityVideo()
                    await call_py.change_stream(
                        chat_id, AudioVideoPiped(url, HighQualityAudio(), hm)
                    )
                pop_an_item(chat_id)
                return [songname, link, type]
            except:
                await call_py.leave_group_call(chat_id)
                clear_queue(chat_id)
                return 2
    else:
        return 0


async def skip_item(chat_id, h):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        try:
            x = int(h)
            songname = chat_queue[x][0]
            chat_queue.pop(x)
            return songname
        except Exception as e:
            print(e)
            return 0
    else:
        return 0


@call_py.on_stream_end()
async def stream_end_handler(_, u: Update):
    if isinstance(u, StreamVideoEnded):
        chat_id = u.chat_id
        print(chat_id)
        op = await skip_current_song(chat_id)
        if op == 1:
            await app.send_message(
                chat_id,
                "**✅ Antrian kosong.\n\n• Assistant meninggalkan obrolan suara**",
            )
        elif op == 2:
            await app.send_message(
                chat_id,
                f"**❌ terjadi kesalahan\n\n» Membersihkan antrian dan keluar dari obrolan video.**",
            )
        else:
            await app.send_message(
                chat_id,
                f"**▷ Sekarang memutar video\n\n🏷 Nama: [{op[0]}]({op[1]})**",
                disable_web_page_preview=True,
                reply_markup=keyboard,
            )


@call_py.on_kicked()
async def kicked_handler(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@call_py.on_closed_voice_chat()
async def closed_voice_chat_handler(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@call_py.on_left()
async def left_handler(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)
