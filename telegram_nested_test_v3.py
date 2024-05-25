import os
from dotenv import load_dotenv
from TinderBot import TinderBot
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from dialog import Dialog
odd_numbers = [num for num in range(3, 51, 2)]
even_numbers = [num for num in range(2, 51, 2)]

env_path = '/home/frank/Documents/Tokens/.env'
load_dotenv(dotenv_path=env_path)
pass
class TelegramBot:
    ITEMS_PER_PAGE = 5
    MAX_LEVELS = 15  # Maximum depth of the menu
    odd_numbers = [num for num in range(3, 51, 2)]
    even_numbers = [num for num in range(2, 51, 2)]
    def __init__(self):
        self.updater = Updater(os.getenv('TELEGRAM_TOKEN'))
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CallbackQueryHandler(self.button))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_custom_text))
        self.tbot = TinderBot()
        self.matches = self.tbot.get_matches()
        self.custom_text = None
        self.selected_match_id = ""
        self.text = ""
        self.current_message = ""
        self.gpt_replies = []
        self.gpt_message = []
        self.level = None
        self.page = None

    def start(self, update: Update, context: CallbackContext) -> None:
        keyboard = self.get_menu(level=1, page=0)
        update.message.reply_text( text = "choose", reply_markup=keyboard)

    def get_menu(self, level, page):
        if(self.level != level) :
            self.gpt_message = []
        self.level = level
        self.page = page
        start_idx = page * self.ITEMS_PER_PAGE
        end_idx = start_idx + self.ITEMS_PER_PAGE
        end_idx = min(end_idx, len(self.gpt_replies) - 1)


    #    if (page) > 0 :
     #       end_idx = min(end_idx,len(self.gpt_replies)-1)

        if self.level == 1:

            matches_dict = self.tbot.get_matches_names()
            matches_names = [item['name'] for item in matches_dict]
            matches_id = [item['id'] for item in matches_dict]
            items = matches_names[start_idx:end_idx]
            ids = matches_id[start_idx:end_idx]
            has_new_messages = [self.tbot.has_new_message(match) for match in matches_id]
            matches = self.matches[start_idx:end_idx]

            buttons = [[InlineKeyboardButton(text=item, callback_data=f"{self.level}_{index}_{self.page}_{id}")] for index,(item, id) in enumerate(zip(items, ids))]

        else :
            items_shown = [self.gpt_replies[i] for i in range(start_idx + 1, end_idx + 1)]
            self.gpt_message = self.gpt_message+items_shown
            pass


            buttons = [
                [InlineKeyboardButton(text=item, callback_data=f"{self.level}_{index}_{self.page}")] for index,item in enumerate(items_shown)
            ]

        buttons.append([InlineKeyboardButton(text="Send Your Text", callback_data=f"{self.level}_custom_{self.page}")])

        # Navigation buttons
        navigation_buttons = []
        if start_idx > 0:
            navigation_buttons.append(InlineKeyboardButton(text="<< Prev", callback_data=f"{self.level}_prev_{self.page - 1}"))
        if end_idx < (len(self.gpt_replies) - 1):
            navigation_buttons.append(InlineKeyboardButton(text="Next >>", callback_data=f"{self.level}_next_{self.page + 1}"))
        if navigation_buttons:
            buttons.append(navigation_buttons)

        return InlineKeyboardMarkup(buttons)
    def from_match_id_to_match_object(self,in_sMatchID):
        for match in self.matches:
            if match.match_id == in_sMatchID:
                return match
        return None  # Return None if match_id is not found in the list
    def get_match_name(self,in_sMatchID):
        item = [item for item in self.matches if item.match_id == in_sMatchID]
        return item.person.name
    def handle_custom_text(self, update: Update, context: CallbackContext) -> None:
        self.custom_text = update.message.text
        update.message.reply_text(f"Received your text: {self.custom_text}")

        # Define the buttons
        yes_button = InlineKeyboardButton(text="Yes", callback_data="0_yes_custom")
        no_button = InlineKeyboardButton(text="No", callback_data="0_no_custom")
        keyboard = InlineKeyboardMarkup([[yes_button, no_button]])

        # Send the buttons as a reply
        update.message.reply_text('Do you want to proceed?', reply_markup=keyboard)
    def run(self):
        self.updater.start_polling()
        self.updater.idle()
    def button(self, update, context) -> None:
        query = update.callback_query
        query.answer()

        data = query.data.split("_")
        if len(data) == 4 :
            self.selected_match_id = data[3]
        action = data[1]


        if action == 'yes':
            self.tbot.send_response(self.custom_text,self.selected_match_id)
            query.edit_message_text(text="Message Sent!")
            return
        if action == 'custom':
            query.edit_message_text(text="Please send your custom text now.")
            return
        else :
            if action != "no" :
                self.level = int(data[0])
                self.page = int(data[2])
            if action in ["next", "prev"]:

                keyboard = self.get_menu(self.level, self.page)
                start_idx = self.page * self.ITEMS_PER_PAGE
                end_idx = min(start_idx + self.ITEMS_PER_PAGE,len(self.gpt_message))

                for idx, part in enumerate(self.gpt_message[start_idx: end_idx]):
                    dv = len(self.gpt_message[start_idx: end_idx-1])
                    pass
                    if idx == len(self.gpt_message[start_idx: end_idx-1]):
                        query.message.reply_text(text=part, reply_markup=keyboard)
                    else:
                        query.message.reply_text(text=part)


            else:
                item = data[1]
                if 'custom' in data :
                    self.level = self.level-1

                if self.level < self.MAX_LEVELS:
                    # click on the text button
                    click_number = data[1]  # i.e more cocky
                    idx_clicked = self.page * self.ITEMS_PER_PAGE + int(click_number)
                    msg_enhancement = None
                    if self.level != 1 :
                        if (self.level + 1) in even_numbers:
                            msg_enhancement = self.gpt_message[int(click_number)]
                        else :
                            self.current_message = self.gpt_message[int(click_number)]
                    if ((self.level) in odd_numbers) or (self.level == 1 ):
                        if(self.level == 1) :
                            self.gpt_replies = self.tbot.chatgpt.invokegpt_first()

                        else :
                            self.gpt_replies = self.tbot.reply_messages_v2(self.from_match_id_to_match_object(self.selected_match_id),self.current_message,msg_enhancement)
                    else :
                        self.gpt_replies = self.tbot.generate_enhancements()

                    keyboard = self.get_menu(self.level + 1, 0)  # Move to the next level
                    if (self.level == 1) :
                        self.text = self.tbot.process_messages(self.selected_match_id)
                    else :
                        self.text = self.current_message
                    text_parts = [self.text[i:i + 4000] for i in
                                  range(0, len(self.text), 4000)]  # Splitting into parts of 4000 characters each
                    '''
                    for part in text_parts:
                        query.edit_message_text(text=part, reply_markup=keyboard)

                else:
                    query.edit_message_text(text=f"You reached the final selection: {item}")

                    #     text_parts = text_parts.reverse()
                    '''
                    # Sending each part as a separate message

                    for part in text_parts:
                        query.message.reply_text(text=part)
                    dv = min(self.ITEMS_PER_PAGE-1, len(self.gpt_message))
                    pass
                    if self.level in odd_numbers :
                        query.message.reply_text(text="A", reply_markup=keyboard)
                    else :
                        for idx,part in enumerate(self.gpt_message[:min(self.ITEMS_PER_PAGE, len(self.gpt_message))]) :

                            if idx == min((self.ITEMS_PER_PAGE-1,len(self.gpt_message)-1)):
                                query.message.reply_text(text= part, reply_markup=keyboard)
                            else :
                                query.message.reply_text(text= part)


                else:
                    query.edit_message_text(text=f"You reached the final selection: {item}")



if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()