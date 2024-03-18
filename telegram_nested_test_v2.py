import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,CallbackContext
load_dotenv('.env')
enhanced_messages = ['More cocky','More funny','More flirty','More dovish']
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

    def get_chatgpt_label(self, level, option_number):
        # Placeholder for generating or retrieving a label from ChatGPT
        # You need to implement this based on your requirement
        return f"ChatGPT Label {level}-{option_number}"
    def get_nested_menu(self, selected_options, current_level) -> InlineKeyboardMarkup:
        # Generate a menu for the current level based on previously selected options
        buttons = []
        for i in range(1, self.ITEMS_PER_PAGE + 1):
            if current_level % 2 == 0:  # Even levels use ChatGPT labels
                label = self.get_chatgpt_label(current_level, i)
            else:  # Odd levels use labels from the custom list
                # Cycle through the custom list if there are more options than list items
                label_index = (i - 1) % len(enhanced_messages)
                label = enhanced_messages[label_index]

            option = '_'.join(selected_options + [f"L{current_level}Opt{i}"])
            buttons.append([InlineKeyboardButton(text=label, callback_data=option)])

        return InlineKeyboardMarkup(buttons)
    def start(self,update: Update, context: CallbackContext) -> None:
        keyboard = self.get_menu(0)

        update.message.reply_text('Choose an option:', reply_markup=keyboard)

    def button(self, update, callback) -> None:
        query = update.callback_query
        query.answer()

        data = query.data
        # Split the callback data to get the selected options and the current level
        selected_options = data.split('_')
        current_level = len(selected_options)

        if current_level <= self.ITEMS_PER_PAGE:
            # Generate the next level menu
            keyboard = self.get_nested_menu(selected_options, current_level)
            query.edit_message_text(text=f"You are at level {current_level}. Choose an option:", reply_markup=keyboard)
        else:
            # Final selection
            query.edit_message_text(text=f"Final selection: {' > '.join(selected_options)}")
    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()