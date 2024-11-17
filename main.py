"""
i want to impliment my note database code with my bot but how?
This is my bot i want to impliment my old note making app connected with 
bot just for leaning, first my code there was just a bot interface connected with my 
database which i need to impliment.
"""

# First Part is for load the private bot token value from .env file
import os
from dotenv import load_dotenv


import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if user:
        text = f"Hello {user.full_name} this is a Example Bot"
        await context.bot.send_message(user.id, text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    if update.message:
        user = update.message.from_user
    else:
        user = None
    text = f"I Have many way first make a user which is you and then " "Make a new note"
    if user:
        await context.bot.send_message(user.id, text)


async def add_me_as_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This will add thsi current user in the database"""


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """I will save this text in teh database against your name"""
    text = "I will save this text in teh database against your name"
    if update.message:
        await update.message.reply_text(text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    if BOT_TOKEN:
        application = Application.builder().token(BOT_TOKEN).build()
    else:
        application = Application.builder().token("RanaUniverse🍌🍌🍌").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
