import os

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus
from telegram.error import Forbidden, BadRequest, TelegramError

from .db_utils import remove_chat
from .inline_result_handlers import inline_result_bet, inline_result_balance, inline_result_roll


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    
    if isinstance(error, Forbidden):
        print("❌ Forbidden: Bot was blocked by a user or removed from a group.")
    elif isinstance(error, BadRequest):
        print(f"⚠️  BadRequest: {error}")
    elif isinstance(error, TelegramError):
        print(f"💥 TelegramError: {error}")
    else:
        print(f"⚠️  Unhandled exception: {error}")


async def handle_bot_member(update: Update, context: ContextTypes.DEFAULT_TYPE):

    new_status = update.my_chat_member.new_chat_member.status
    old_status = update.my_chat_member.old_chat_member.status

    if new_status == ChatMemberStatus.MEMBER and old_status == ChatMemberStatus.LEFT:
        text = 'This is a simple betting bot.'
        text += f'\nTo roll for your daily amount of units, use the command /roll or select the inline button after typing {os.getenv('BOT_TAG')}'
        text += f'\nTo place a bet, use the command /bet <amount> or use the inline query: {os.getenv('BOT_TAG')} <amount>'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    elif new_status == ChatMemberStatus.LEFT and old_status == ChatMemberStatus.MEMBER:
        #delete from db chat_id for this chat
        remove_chat(update.effective_chat.id)
        pass


async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    
    if (not query) or (not query.isnumeric()):
        await update.inline_query.answer([
                                            inline_result_bet(update, 5),
                                            inline_result_balance(update)
                                        ], 
                                        cache_time=1
                                        )
        return

    results = [
        inline_result_bet(update, query),
        inline_result_balance(update),
        inline_result_roll(update)
    ]

    await update.inline_query.answer(results, cache_time=1)