from pyrogram import Client, filters
import asyncio
import os
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from youtubesearchpython import VideosSearch
from AlexaSongBot.mrdarkprince import get_arg
from AlexaSongBot import app, LOGGER
from AlexaSongBot.sql.chat_sql import add_chat_to_db


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


@app.on_message(filters.command("song"))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    add_chat_to_db(str(chat_id))
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("🆙 Mahnı adı daxil edin")
        return ""
    video_link = yt_search(args)
    if not video_link:
        await message.reply("😔 Mahnı tapılmadı.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await message.reply("Xəta baş verdi")
        LOGGER.error(ex)
        return ""
    rename = os.rename(download, f"{str(user_id)}.m4a")
    await app.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.m4a",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str("Hüsü"),
        reply_to_message_id=message.message_id,
    )
    os.remove(f"{str(user_id)}.m4a")
