import logging
import signal
import asyncio
from dotenv import load_dotenv
import os
from sqlalchemy.exc import OperationalError

from telegram.ext import Application,ApplicationBuilder, CommandHandler,Application,CallbackQueryHandler, ChatMemberHandler,InlineQueryHandler

from database import init_db,Engine,ScopedSession
from create_db import create_database

from utils.command_handlers import app_start, app_bet, app_balance, app_roll
from utils.db_utils import remove_chat
from utils.callback_handlers import callback_bet_handler
from utils.generic_handlers import error_handler, handle_bot_member, inline_query_handler

# Database setup
try:
    init_db()

except OperationalError as e:
    print(f"Error database not found. Creating tables...")
    try:
        create_database()
        init_db()
    except Exception as e:
        print(f"Error creating database: {e}")
        exit(0)

except Exception as e:
    print(f"Error initializing database: {e}")
    exit(0)


# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



# Telegram bot setup functions
async def app_add_handlers(application):
    start_handler = CommandHandler('start', app_start)
    bet_handler = CommandHandler('bet', app_bet)
    balance_handler = CommandHandler('balance', app_balance)
    roll_handler = CommandHandler('roll', app_roll)  # Placeholder for roll command
    group_add_handler = ChatMemberHandler(handle_bot_member, chat_member_types=ChatMemberHandler.MY_CHAT_MEMBER)
    
    application.add_handler(start_handler)
    application.add_handler(group_add_handler)
    application.add_handler(bet_handler)
    application.add_handler(balance_handler)
    application.add_handler(roll_handler)
    application.add_handler(InlineQueryHandler(inline_query_handler))
    application.add_handler(CallbackQueryHandler(callback_bet_handler, pattern=r"^bet_(\d+)_(\d+)_(.+)$"))

    application.add_error_handler(error_handler)

    await application.bot.set_my_commands([
        ('bet', 'Place a bet'),
        ('balance', 'Check your balance'),
        ('roll', 'Roll for daily units'),
    ])

    # application.add_handler(message_handler)
    
async def app_start(application: Application):
    await application.initialize()
    await application.start()
    await application.updater.start_polling()


# Main
async def main():
    try:
        application = (ApplicationBuilder().token(os.getenv('BOT_TOKEN'))
            .get_updates_read_timeout(30)
            .get_updates_connect_timeout(30)
            .get_updates_write_timeout(30)
            .build())
        
        await app_add_handlers(application)
        
        await app_start(application)
        
        # Start other asyncio frameworks here    
        #
        #
        
        # Add some logic that keeps the event loop running until you want to shutdown
        while not stop.is_set():
            try:
                await asyncio.sleep(2)
            except (KeyboardInterrupt,asyncio.CancelledError):
                break
        
        # scheduler.shutdown(wait=True)
        try:
            # Stop the other asyncio frameworks here
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
            ScopedSession.remove()
            Engine.dispose()

        except Exception as e:
            print(e)
            
    except Exception as e:
        print(e)
        logging.error(f"Error in main: {e}")


# Entry point
def signal_handler(signum, frame):
    print("Received signal: ", signum)
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(stop.set)
stop = asyncio.Event()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(main())