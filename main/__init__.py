# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from config import API_ID, API_HASH, BOT_TOKEN, FORCE_SUB
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Bot(Client):

    def __init__(self):
        super().__init__(
            "techvj login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=50,
            sleep_threshold=10
        )

      
    async def start(self):
            
        await super().start()
        print('✔️ Bot Started Modified By 𝐖𝐎𝐎𝐃𝐜𝐫𝐚𝐟𝐭')

    async def stop(self, *args):

        await super().stop()
        print('Bot Stopped Bye')

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def force_sub(bot, update):
    try:
        user = await bot.get_chat_member(FORCE_SUB, update.from_user.id)
        if user.status == "kicked":
            await update.reply_text("Sorry Sir, You are Banned to use me. Contact admin")
            return 400
    except UserNotParticipant:
        await update.reply_text(
            text=f"**Please Join My Update Channel to use this Bot!**\n\n**Due to Overload, Only Channel Subscribers can use the Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{FORCE_SUB}")
                    ]
                ]
            )
        )
        return 400
    except Exception:
        await update.reply_text("Something went wrong. Contact admin")
        return 400

@Client.on_message(filters.private & (filters.command("start") | filters.regex("^(?!/start$).*")) & ~filters.edited)
async def start(bot, message):
    
    # Check Force Sub or Handle /start
    if message.text == "/start":
        res = await force_sub(bot, message)
        if res == 400:
            return
    else:
        res = await force_sub(bot, message)
        if res == 400:
            return

    await message.reply_text(
        text="Hello {} 👋".format(message.from_user.mention)
    )
