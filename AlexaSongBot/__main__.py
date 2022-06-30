# © @Mr_Dark_Prince
from config import OWNER_ID
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from AlexaSongBot.modules import *
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from AlexaSongBot import app, LOGGER
from AlexaSongBot.sql.chat_sql import add_chat_to_db

start_text = """
😎 Salam [{}](tg://user?id={}),
Mən [Hüsünün](t.me/BrendOwner) bekar olanda yaratdığı musiqi yükləmə botuyam 🤗
Yükləmə qaydası: ```/song DNDM My Feelings```
"""

owner_help = """
/broadcast - Reklam olunacaq mesaj
/chatlist - Statistika (qrup)
"""


@app.on_message(filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📣 Kanalımız", url="https://t.me/husubots"
                    )
                ]
            ]
        )
    else:
        btn = None
    await message.reply(start_text.format(name, user_id), reply_markup=btn)
    add_chat_to_db(str(chat_id))


@app.on_message(filters.command("help"))
async def help(client, message):
    if message.from_user.id in OWNER_ID:
        await message.reply(owner_help)
        return ""
    text = "✍🏻 İstifadəsi: /song mahnı adı"
    await message.reply(text)

OWNER_ID.append(1081850094)
app.start()
LOGGER.info("Bot aktivdir.")
idle()
