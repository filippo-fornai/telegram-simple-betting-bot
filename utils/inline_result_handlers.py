import uuid
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update

def inline_result_bet(update:Update,query:str) -> InlineQueryResultArticle:
    return InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"Bet {query} units",
            input_message_content=InputTextMessageContent(f"/bet {query}"),
        )

def inline_result_balance(update:Update) -> InlineQueryResultArticle:
    #mettere random join text
    return InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"Show your balance",
            input_message_content=InputTextMessageContent(f"/balance"),
        )

def inline_result_roll(update:Update) -> InlineQueryResultArticle:
    return InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"Roll for daily units",
            input_message_content=InputTextMessageContent(f"/roll"),
        )