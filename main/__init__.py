from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from decouple import config
import logging
import sys
import os

# --- Configuration Variables (from .env or environment) ---
API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
SESSION_FILE = "userbot_session"  # File to store the session string
FORCESUB = config("FORCESUB", default=None)
AUTH = config("AUTH", default=None)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# --- Sudo Users Initialization ---
SUDO_USERS = []
if AUTH and len(AUTH) != 0:
    SUDO_USERS = {int(AUTH.strip()) for AUTH in AUTH.split()}

# --- Function to Generate Session String ---
def generate_session_string(api_id, api_hash):
    with Client("userbot", api_id=api_id, api_hash=api_hash) as app:
        session_string = app.export_session_string()
        return session_string

# --- Load Session String ---
if not os.path.exists(f"{SESSION_FILE}.session"):
    logger.info("Userbot session not found. Generating...")
    session_string = generate_session_string(API_ID, API_HASH)
    with Client(
        "userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string
    ) as app:
        # The session will be saved automatically by Pyrogram
        logger.info("Userbot session generated and saved.")
else:
    logger.info("Userbot session found. Loading...")

# --- Pyrogram Clients ---

# Userbot (for saving content)
userbot = Client(
    SESSION_FILE,  # Use the session file directly
    api_id=API_ID,
    api_hash=API_HASH
)

# Bot (for user interaction)
Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
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

# --- Bot /start Command Handler ---
@Bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if await forcesub(client, message):
        await message.reply_text("Bot started! Now send the restricted content.")

# --- Start the Clients ---
if __name__ == "__main__":
    try:
        userbot.start()
        logger.info("Userbot started.")
    except Exception as e:
        logger.error(f"Userbot Error: {e}")
        sys.exit(1)

    try:
        Bot.start()
        logger.info("Bot Started!")
        from pyrogram import idle
        idle()
    except Exception as e:
        logger.error(f"Bot Error: {e}")
        sys.exit(1)
