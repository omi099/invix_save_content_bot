from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from decouple import config
import logging, time, sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)

# variables
API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
SESSION = config("SESSION", default=None)
FORCESUB = config("FORCESUB", default=None)
AUTH = config("AUTH", default=None)
SUDO_USERS = []
if len(AUTH) != 0:
    SUDO_USERS = {int(AUTH.strip()) for AUTH in AUTH.split()}
else:
    SUDO_USERS = set()

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

userbot = Client("myacc", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

try:
    userbot.start()
except BaseException:
    print("Userbot Error ! Have you added SESSION while deploying??")
    sys.exit(1)

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)

# Force Subscribe
async def forcesub(bot: Client, update):
    if FORCESUB:
        try:
            await bot.get_chat_member(FORCESUB, update.from_user.id)
        except Exception as e:
            
            button = [[InlineKeyboardButton(text="Join Channel", url=f"https://t.me/{FORCESUB}")]]
            markup = InlineKeyboardMarkup(button)
            await update.reply_text(
                text=f"You must join @{FORCESUB} to use this bot.",
                reply_markup=markup,
                quote=True
            )
            return False
    return True

# Bot start handler with Force Subscribe check
@Bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if await forcesub(client, message):
        await message.reply_text("Bot started! Now send the restricted content.")
        

try:
    Bot.start()
    logger.info("Bot Started!")
except Exception as e:
    logger.info(e)
    sys.exit(1)

Bot.run()
