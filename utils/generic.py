from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError

async def delete_massage(update:Update):
    try:
        await update.message.delete()        # ⇐ preferred API :contentReference[oaicite:1]{index=1}
    except TelegramError as e:
        print(f"Error deleting message: {e}")
        pass  # silently ignore if we lack rights