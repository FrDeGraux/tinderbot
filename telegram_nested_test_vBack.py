from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from dotenv import load_dotenv

env_path = '/home/frank/Documents/Tokens/.env'
load_dotenv(dotenv_path=env_path)
# Sample list of items to search from
items = [
    "apple",
    "banana",
    "cherry",
    "date",
    "fig",
    "grape",
    "kiwi"
]


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Type anything to search items.')


def search_items(query):
    query = query.lower()
    matching_items = [item for item in items if query in item.lower()]
    return matching_items


def handle_message(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    matching_items = search_items(query)

    if matching_items:
        response = "Found the following items:\n" + "\n".join(matching_items)
    else:
        response = "No matching items found."

    update.message.reply_text(response)


def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(os.getenv('TELEGRAM_TOKEN'))
    dp = updater.dispatcher

    # Add handlers for the start command and text messages
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
