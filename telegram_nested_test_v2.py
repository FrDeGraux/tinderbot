import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

load_dotenv('.env')


class TelegramBot:
    ITEMS_PER_PAGE = 5
    MAX_LEVELS = 5  # Maximum depth of the menu

    def __init__(self):
        self.updater = Updater(os.getenv('TELEGRAM_TOKEN'))
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CallbackQueryHandler(self.button))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_custom_text))

    def start(self, update: Update, context: CallbackContext) -> None:
        keyboard = self.get_menu(level=1, page=0)
        update.message.reply_text('Choose an option:', reply_markup=keyboard)

    def get_menu(self, level, page):
        start_idx = page * self.ITEMS_PER_PAGE
        end_idx = start_idx + self.ITEMS_PER_PAGE

        if level == 1:
            items = [f"Option{i}" for i in range(start_idx + 1, end_idx + 1)]
        elif level in [2, 4, 5]:
            items = [f"ChatGPTLabel{i}" for i in range(start_idx + 1, end_idx + 1)]
        elif level == 3:
            items = [f"Cocky{i}" for i in range(start_idx + 1, end_idx + 1)]

        buttons = [
            [InlineKeyboardButton(text=item, callback_data=f"{level}_{item}_{page}")] for item in items
        ]
        buttons.append([InlineKeyboardButton(text="Send Your Text", callback_data=f"{level}_custom_{page}")])

        # Navigation buttons
        navigation_buttons = []
        if start_idx > 0:
            navigation_buttons.append(InlineKeyboardButton(text="<< Prev", callback_data=f"{level}_prev_{page - 1}"))
        navigation_buttons.append(InlineKeyboardButton(text="Next >>", callback_data=f"{level}_next_{page + 1}"))
        if navigation_buttons:
            buttons.append(navigation_buttons)

        return InlineKeyboardMarkup(buttons)

    def handle_custom_text(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        update.message.reply_text(f"Received your text: {text}")

        # Define the buttons
        yes_button = InlineKeyboardButton(text="Yes", callback_data="0_yes")
        no_button = InlineKeyboardButton(text="No", callback_data="0_no")
        keyboard = InlineKeyboardMarkup([[yes_button, no_button]])

        # Send the buttons as a reply
        update.message.reply_text('Do you want to proceed?', reply_markup=keyboard)

    def button(self, update, context) -> None:
        query = update.callback_query
        query.answer()

        data = query.data.split("_")
        action = data[1]

        if action == 'yes':
            query.edit_message_text(text="Message Sent!")
            return
        elif action == 'custom':
            query.edit_message_text(text="Please send your custom text now.")
            return
        elif action in ["next", "prev"]:
            level = int(data[0])
            page = int(data[2])
            keyboard = self.get_menu(level, page)
            query.edit_message_text(text=f"Level {level} - Choose an option:", reply_markup=keyboard)
        else:
            level = int(data[0])
            item = data[1]
            page = int(data[2])
            if level < self.MAX_LEVELS:
                keyboard = self.get_menu(level + 1, 0)  # Move to the next level
                query.edit_message_text(text=f"Level {level + 1} - You selected {item}. Choose a sub-option:",
                                        reply_markup=keyboard)
            else:
                query.edit_message_text(text=f"You reached the final selection: {item}")

    def run(self):
        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
