from config import OWNER_ID
from pyrogram import filters
from AlexaSongBot import app
from AlexaSongBot.mrdarkprince import get_arg
from AlexaSongBot.sql.chat_sql import load_chats_list, remove_chat_from_db
from io import BytesIO


@app.on_message(filters.user(OWNER_ID) & filters.command("broadcast"))
async def broadcast(client, message):
    to_send = get_arg(message)
    chats = load_chats_list()
    success = 0
    failed = 0
    for chat in chats:
        try:
            await app.send_message(int(chat), to_send)
            success += 1
        except:
            failed += 1
            remove_chat_from_db(str(chat))
            pass
    await message.reply(f"🙂 Reklam tamamlandı\n\n✅ {success} söhbətə göndərildi.\n❌ {failed} söhbətə göndərilmədi")


@app.on_message(filters.user(OWNER_ID) & filters.command("chatlist"))
async def chatlist(client, message):
    chats = []
    all_chats = load_chats_list()
    for i in all_chats:
        if str(i).startswith("-"):
            chats.append(i)
    chatfile = "Qrup siyahısı.\n0. Qrup ID | İstifadəçi sayı | Dəvət linki\n"
    P = 1
    for chat in chats:
        try:
            link = await app.export_chat_invite_link(int(chat))
        except:
            link = "Yoxdur"
        try:
            members = await app.get_chat_members_count(int(chat))
        except:
            members = "Yoxdur"
        try:
            chatfile += "{}. {} | {} | {}\n".format(P, chat, members, link)
            P = P + 1
        except:
            pass
    with BytesIO(str.encode(chatfile)) as output:
        output.name = "HusuStatd.txt"
        await message.reply_document(document=output, disable_notification=True)
