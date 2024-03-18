import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,CallbackContext
load_dotenv('.env')

class TelegramBot:
    ITEMS_PER_PAGE = 5

    def __init__(self):
        self.items = [f"Option {i}" for i in range(1, 21)]
        self.updater = Updater(os.getenv('TELEGRAM_TOKEN'))
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('custommessage', self.custom_message))
        dp.add_handler(CallbackQueryHandler(self.button))

    def custom_message(self,update, callback,msg ) -> None:
        keyboard = [[InlineKeyboardButton(text="Show Options", callback_data="show_options")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            msg + ' lick below to see the options:',
            reply_markup=reply_markup)

    def get_menu(self, page: int) -> InlineKeyboardMarkup:
        '''get_menu: This method generates an inline keyboard markup for pagination. It creates buttons for the current set of items and, if necessary, navigation buttons for previous and next pages.'''
        start_idx = page * self.ITEMS_PER_PAGE
        end_idx = start_idx + self.ITEMS_PER_PAGE
        current_items = self.items[start_idx:end_idx]

        buttons = [
            [InlineKeyboardButton(text=item, callback_data=item)] for item in current_items
        ]

        # Navigation buttons
        if start_idx > 0:
            buttons.append([InlineKeyboardButton(text="<< Prev", callback_data=f"prev_{page}")])
        if end_idx < len(self.items):
            buttons.append([InlineKeyboardButton(text="Next >>", callback_data=f"next_{page}")])

        return InlineKeyboardMarkup(buttons)

    def start(self,update: Update, context: CallbackContext) -> None:
        keyboard = self.get_menu(0)

        update.message.reply_text('Choose an option:', reply_markup=keyboard)

    def button(self, update, callback) -> None:
        query = update.callback_query
        query.answer()

        data = query.data
        if data == "show_options":
            keyboard = self.get_menu(0)
            query.edit_message_text(text="Choose an option:", reply_markup=keyboard)
        elif data.startswith("next_"):
            _, page = data.split("_")
            keyboard = self.get_menu(int(page) + 1)
            query.edit_message_text(text="Choose an option:", reply_markup=keyboard)
        elif data.startswith("prev_"):
            _, page = data.split("_")
            keyboard = self.get_menu(int(page) - 1)
            query.edit_message_text(text="Choose an option:", reply_markup=keyboard)
        elif data.startswith("Option"):  # This is a new block to handle selected options
            self.handle_option_selection(query, data)
        else:
            # Process other callback data
            query.edit_message_text(text=f"You selected {data}")

    def handle_option_selection(self, query, data) -> None:
        # Assuming `data` is something like "Option 1", extract the option number
        option_number = data.split(" ")[-1]
        # Generate a new set of buttons based on the selected option
        keyboard = self.get_secondary_menu(option_number)
        query.edit_message_text(text=f"You selected {data}. Now choose a sub-option:", reply_markup=keyboard)

    def get_secondary_menu(self, option_number: str) -> InlineKeyboardMarkup:
        # Generate a secondary menu based on the option number. This is just an example.
        sub_options = [f"Sub-option {option_number}.{i}" for i in range(1, 4)]  # Create 3 sub-options
        buttons = [
            [InlineKeyboardButton(text=sub_option, callback_data=sub_option)] for sub_option in sub_options
        ]
        return InlineKeyboardMarkup(buttons)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()