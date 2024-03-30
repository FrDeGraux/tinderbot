import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
load_dotenv('.env')

class TelegramBot:
    ITEMS_PER_PAGE = 5

    def __init__(self):
        self.items = [f"Option {i}" for i in range(1, 21)]
        self.updater = Updater(os.getenv('TELEGRAM_TOKEN'))
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CallbackQueryHandler(self.button))

    def start(self, update: Update, context: CallbackContext) -> None:
        keyboard = self.get_menu(0)
        update.message.reply_text('Choose an option:', reply_markup=keyboard)

    def get_menu(self, page: int) -> InlineKeyboardMarkup:
        start_idx = page * self.ITEMS_PER_PAGE
        end_idx = start_idx + self.ITEMS_PER_PAGE
        current_items = self.items[start_idx:end_idx]

        buttons = [
            [InlineKeyboardButton(text=item, callback_data=item)] for item in current_items
        ]

        if start_idx > 0:
            buttons.append([InlineKeyboardButton(text="<< Prev", callback_data=f"prev_{page}")])
        if end_idx < len(self.items):
            buttons.append([InlineKeyboardButton(text="Next >>", callback_data=f"next_{page}")])

        return InlineKeyboardMarkup(buttons)

    def button(self, update, context) -> None:
        query = update.callback_query
        query.answer()

        data = query.data

        if data.startswith("next_"):
            _, page = data.split("_")
            keyboard = self.get_menu(int(page) + 1)
            query.edit_message_text(text="Choose an option:", reply_markup=keyboard)
        elif data.startswith("prev_"):
            _, page = data.split("_")
            keyboard = self.get_menu(int(page) - 1)
            query.edit_message_text(text="Choose an option:", reply_markup=keyboard)
        elif data.startswith("Option"):
            self.handle_option_selection(query, data)
        elif data.startswith("sub_next_") or data.startswith("sub_prev_"):
            self.handle_secondary_navigation(query, data)
        else:
            query.edit_message_text(text=f"You selected {data}")

    def handle_option_selection(self, query, data):
        option_number = data.split(" ")[-1]
        keyboard = self.get_secondary_menu(option_number, 0)
        query.edit_message_text(text=f"You selected {data}. Now choose a sub-option:", reply_markup=keyboard)

    def get_secondary_menu(self, option_number: str, page: int, total_sub_options: int = 10) -> InlineKeyboardMarkup:
        start_idx = page * self.ITEMS_PER_PAGE
        end_idx = min(start_idx + self.ITEMS_PER_PAGE, total_sub_options)

        sub_options = [f"Sub-option {option_number}.{i}" for i in range(start_idx + 1, end_idx + 1)]

        buttons = [
            [InlineKeyboardButton(text=sub_option, callback_data=sub_option)] for sub_option in sub_options
        ]

        if start_idx > 0:
            buttons.append([InlineKeyboardButton(text="<< Prev", callback_data=f"sub_prev_{option_number}_{page}")])
        if end_idx < total_sub_options:
            buttons.append([InlineKeyboardButton(text="Next >>", callback_data=f"sub_next_{option_number}_{page}")])

        return InlineKeyboardMarkup(buttons)

    def handle_secondary_navigation(self, query, data):
        _, direction, option_number, page = data.split("_")
        new_page = int(page) + 1 if direction == "next" else int(page) - 1
        keyboard = self.get_secondary_menu(option_number, new_page)
        query.edit_message_text(text=f"Option {option_number}. Choose a sub-option:", reply_markup=keyboard)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
