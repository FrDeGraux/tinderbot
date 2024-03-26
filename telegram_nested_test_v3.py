import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

load_dotenv('.env')

enhanced_messages = ['More cocky', 'More funny', 'More flirty', 'More dovish']

class TelegramBot:
    ITEMS_PER_PAGE = 5

    def __init__(self):
        self.items = [f"Option {i}" for i in range(1, 21)]
        self.updater = Updater(os.getenv('TELEGRAM_TOKEN'))
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CallbackQueryHandler(self.button))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_custom_text))

    def get_menu(self, page: int) -> InlineKeyboardMarkup:
        start_idx = page * self.ITEMS_PER_PAGE
        end_idx = start_idx + self.ITEMS_PER_PAGE
        current_items = self.items[start_idx:end_idx]

        buttons = [
            [InlineKeyboardButton(text=item, callback_data=item)] for item in current_items
        ]

        buttons.append([InlineKeyboardButton(text="Send Your Text", callback_data="custom_text")])

        if start_idx > 0:
            buttons.append([InlineKeyboardButton(text="<< Prev", callback_data=f"prev_{page}")])
        if end_idx < len(self.items):
            buttons.append([InlineKeyboardButton(text="Next >>", callback_data=f"next_{page}")])

        return InlineKeyboardMarkup(buttons)

    def get_nested_menu(self, selected_options, current_level) -> InlineKeyboardMarkup:
        buttons = []
        for i in range(1, self.ITEMS_PER_PAGE + 1):
            if current_level % 2 == 0:
                label = self.get_chatgpt_label(current_level, i)
            else:
                label_index = (i - 1) % len(enhanced_messages)
                label = enhanced_messages[label_index]

            option = '_'.join(selected_options + [f"L{current_level}Opt{i}"])
            buttons.append([InlineKeyboardButton(text=label, callback_data=option)])

        buttons.append([InlineKeyboardButton(text="Send Your Text", callback_data="custom_text")])

        return InlineKeyboardMarkup(buttons)

    def start(self, update: Update, context: CallbackContext) -> None:
        keyboard = self.get_menu(0)
        update.message.reply_text('Choose an option:', reply_markup=keyboard)


    def button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        data = query.data

        if data == 'custom_text':
            query.edit_message_text(text="Please send your custom text now.")
            return
        elif data == 'yes':
            query.edit_message_text(text="Sent message")
            return  # Stop further processing to prevent nesting

        text_data_list = [item for item in query.message.reply_markup.inline_keyboard if item[0]['callback_data'] == query.data]

        if text_data_list:
            text_data = text_data_list[0][0]['text']
        else:
            text_data = ""

        selected_options = data.split('_')
        current_level = len(selected_options)

        if current_level <= self.ITEMS_PER_PAGE:
            keyboard = self.get_nested_menu(selected_options, current_level)
            query.edit_message_text(text=f"You chose {text_data}. Choose an option:", reply_markup=keyboard)
        else:
            query.edit_message_text(text=f"Final selection: {' > '.join(selected_options)}")

    def handle_custom_text(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        update.message.reply_text(f"Received your text: {text}")

        # Define the buttons
        yes_button = InlineKeyboardButton(text="Yes", callback_data="yes")
        no_button = InlineKeyboardButton(text="No", callback_data="no")
        keyboard = InlineKeyboardMarkup([[yes_button, no_button]])

        # Send the buttons as a reply
        update.message.reply_text('Do you want to proceed?', reply_markup=keyboard)

    def get_chatgpt_label(self, level, option_number):
        return f"ChatGPT Label {level}-{option_number}"

    def run(self):
        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
