import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

load_dotenv('.env')


class TelegramBot:
    ITEMS_PER_PAGE = 5
    MAX_LEVELS = 5  # Maximum depth of the menu

    def __init__(self):
        self.updater = Updater(os.getenv('TELEGRAM_TOKEN'))
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CallbackQueryHandler(self.button))

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

        # Navigation buttons
        navigation_buttons = []
        if start_idx > 0:
            navigation_buttons.append(InlineKeyboardButton(text="<< Prev", callback_data=f"{level}_prev_{page - 1}"))
        navigation_buttons.append(InlineKeyboardButton(text="Next >>", callback_data=f"{level}_next_{page + 1}"))
        if navigation_buttons:
            buttons.append(navigation_buttons)

        return InlineKeyboardMarkup(buttons)

    def button(self, update, context) -> None:
        query = update.callback_query
        query.answer()

        data = query.data.split("_")
        level = int(data[0])
        action = data[1]

        if action in ["next", "prev"]:
            page = int(data[2])
            keyboard = self.get_menu(level, page)
            query.edit_message_text(text=f"Level {level} - Choose an option:", reply_markup=keyboard)
        else:
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
