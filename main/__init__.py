from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant

from decouple import config
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# --- Configuration Variables ---
API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
SESSION = config("SESSION", default=None)
FORCESUB = config("FORCESUB", default=None)  # Username of the channel (without @)
AUTH = config("AUTH", default=None)
SUDO_USERS = []
if len(AUTH) != 0:
    SUDO_USERS = {int(AUTH.strip()) for AUTH in AUTH.split()}
else:
    SUDO_USERS = set()

# --- Pyrogram Clients ---
userbot = Client(
    "myacc",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

try:
    userbot.start()
except BaseException:
    logger.error("Userbot Error! Have you added SESSION while deploying??")
    sys.exit(1)

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)

# --- Force Subscribe Function ---
async def forcesub(bot: Client, update):
    if FORCESUB:
        try:
            user_status = await bot.get_chat_member(FORCESUB, update.from_user.id)
            if user_status.status in ("left", "banned"):
                raise UserNotParticipant()
        except UserNotParticipant:
            button = [
                [InlineKeyboardButton(text="Join Channel", url=f"https://t.me/{FORCESUB}")]
            ]
            markup = InlineKeyboardMarkup(button)
            await update.reply_text(
                text=f"You must join @{FORCESUB} to use this bot.",
                reply_markup=markup,
                quote=True
            )
            return False
        except Exception as e:
            logger.error(f"Error in forcesub: {e}")
            await update.reply_text(
                "Something went wrong. Please try again later or contact the bot owner.",
                quote=True
            )
            return False
    return True

# --- Bot Start Handler ---
@Bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if await forcesub(client, message):
        await message.reply_text("Bot started! Now send the restricted content.")

# --- Main Execution ---
if __name__ == "__main__":
    try:
        Bot.start()
        logger.info("Bot Started!")
        from pyrogram import idle
        idle()  # Keep the bot running
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)
