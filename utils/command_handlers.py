# Telegram bot handlers
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from .generic import delete_massage
from .db_utils import build_user, get_user
import random
from datetime import datetime
from database import ScopedSession
from telegram.constants import ParseMode

# Utility
def close_session(session):
    session.commit()
    session.close()

async def app_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Hello. This is a betting bot created for group use. To use it, please add me to your group and give me admin rights."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    
async def app_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    args = context.args
    if len(args) != 1 or not args[0].isnumeric():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /bet <amount>")
        await delete_massage(update)
        return

    session = ScopedSession()    

    amount = int(args[0])
    user=get_user(session,update.effective_user.id, update.effective_chat.id)
    if user is None or user.balance < amount:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"*Sorry {update.effective_user.username} :\\(*\nYou don't have enough units to place a bet of *{amount}*\\.",
                                       parse_mode=ParseMode.MARKDOWN_V2)
        await delete_massage(update)
        close_session(session)
        return
    
    user.balance -= amount

    #logica del bet
    join_text = "🎲 Join Bet 🎲"
    await context.bot.send_message(
                                    chat_id=update.effective_chat.id,
                                    text=f"A bet of *{amount}* units was placed by {update.effective_user.username}\\!",
                                    parse_mode=ParseMode.MARKDOWN_V2,
                                    reply_markup=InlineKeyboardMarkup(
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(
                                                    text=f"{join_text}",
                                                    callback_data=f"bet_{amount}_{user.user_id}_{update.effective_user.username}"
                                                )
                                            ]
                                        ]
                                    )
                                    )
    await delete_massage(update)

    # Session commit and close
    close_session(session)

async def app_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = ScopedSession()

    user = get_user(session,update.effective_user.id, update.effective_chat.id)
    amount = 0 if user is None else user.balance
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=f"*{update.effective_user.username}*'s balance is *{amount}* units\\.",
                                   parse_mode=ParseMode.MARKDOWN_V2
                                   )
    await delete_massage(update)

    close_session(session)
    
    

async def app_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = ScopedSession()

    user = get_user(session,update.effective_user.id, update.effective_chat.id)

    now = datetime.now()

    if user is None:
        amount = random.randint(1, 15)
        new_user = build_user(update.effective_user.id, update.effective_chat.id, amount, now)
        session.add(new_user)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"*Welcome {update.effective_user.username}\\!*\nYou rolled and received *{amount}* units\\.",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await delete_massage(update)

        close_session(session)
        return

    elapsed = (now - user.last_roll).total_seconds()
    if elapsed < 5:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⏳ Please wait *{int(5 - elapsed)} more seconds* before rolling again\\.",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await delete_massage(update)

        close_session(session)
        return

    amount = random.randint(1, 15)
    user.balance += amount
    user.last_roll = now

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"*{update.effective_user.username}* rolled and received *{amount}* units\\. New balance: *{user.balance}* units\\.",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await delete_massage(update)

    # Session commit and close
    close_session(session)
