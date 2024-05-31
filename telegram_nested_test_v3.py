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
        if not (self.level == 1):

            end_idx = min(end_idx, len(self.gpt_replies) - 1)



        if self.level == 1:

            matches_dict = self.tbot.get_matches_names()
            matches_names = [item['name'] for item in matches_dict]
            matches_id = [item['id'] for item in matches_dict]


            items = matches_names[start_idx:end_idx]
            ids = matches_id[start_idx:end_idx]
            items = [(item + " (New) ") if self.tbot.is_a_new_match(id) else item for (id,item) in zip(ids,items)]
            items = [(item + " (To You) ") if (self.tbot.has_new_message(id) and "New" not in item) else item for (id,item) in zip(ids,items)]

            matches = self.matches[start_idx:end_idx]

            buttons = [[InlineKeyboardButton(text=item, callback_data=f"{self.level}_{index}_{self.page}_{id}")] for index,(item, id) in enumerate(zip(items, ids))]

        else :
            items_shown = [self.gpt_replies[i] for i in range(start_idx + 1, end_idx + 1)]
            self.gpt_message = self.gpt_message+items_shown
            pass


            buttons = [
                [InlineKeyboardButton(text=item, callback_data=f"{self.level}_{index}_{self.page}")] for index,item in enumerate(items_shown)
            ]
        if (self.level in odd_numbers) :
            buttons.append(
                [InlineKeyboardButton(text="Send Enhancement", callback_data=f"{self.level}_enhance_{self.page}")])
            buttons.append([InlineKeyboardButton(text="Send Your Text Straight", callback_data=f"{self.level}_custom_{self.page}")])

        if self.level > 1 :
            buttons.append([InlineKeyboardButton(text="Back Level", callback_data=f"{self.level}_backlevel_{self.page}")])


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
        text =  update.message.text
        if self.level in odd_numbers :
            self.msg_enhancement = update.message.text
        else :
            self.custom_text = update.message.text
        update.message.reply_text(f"Received your text: {text}")

        # Define the buttons
        yes_button = InlineKeyboardButton(text="Yes", callback_data="0_yes_custom")
        no_button = InlineKeyboardButton(text="No", callback_data="0_no_custom")
        keyboard = InlineKeyboardMarkup([[yes_button, no_button]])

        # Send the buttons as a reply
        update.message.reply_text('Do you want to proceed?', reply_markup=keyboard)



    def run(self):
        self.updater.start_polling()
        self.updater.idle()
    def complete_action(self,query):

            self.tbot.send_response(self.custom_text, self.selected_match_id)
            query.edit_message_text(text="Message Sent!")
            return

    def invite_to_send_message(self,query):
        query.edit_message_text(text="Please send your custom text now.")
        return
    def act_on_page_change(self,query):
        keyboard = self.get_menu(self.level, self.page)
        start_idx = self.page * self.ITEMS_PER_PAGE
        if self.level > 1  :
            end_idx = min(start_idx + self.ITEMS_PER_PAGE, len(self.gpt_message))
        else :
            end_idx = start_idx + self.ITEMS_PER_PAGE
        if self.level == 1 :
            query.message.reply_text(text="A", reply_markup=keyboard)

        if self.level in odd_numbers:
            query.message.reply_text(text=self.current_message, reply_markup=keyboard)
        else:
            for idx, part in enumerate(self.gpt_message[start_idx:end_idx]):
                pass

                if idx == len(self.gpt_message[start_idx:end_idx - 1]):
                    query.message.reply_text(text=part, reply_markup=keyboard)
                else:
                    query.message.reply_text(text=part)
        return
    def act_on_click(self,data):
        # populate current_message or msg_enhancement
        if self.level < self.MAX_LEVELS:
            # click on the text button
            click_number = data[1]
            idx_clicked = self.page * self.ITEMS_PER_PAGE + int(click_number)
            if self.level in even_numbers:
                self.current_message = self.gpt_message[int(click_number)]
            elif self.level in odd_numbers :
                self.msg_enhancement = self.gpt_message[int(click_number)]


        # will pick the button content to generate further
    def generate_future_buttons_content_from_choices(self):
        # generate future GPT Replies to be displayed
        if (self.level in odd_numbers) or (self.level == 1):
            if self.level == 1:
                self.gpt_replies = self.tbot.chatgpt.invokegpt_first()
            elif self.level == 3:
                self.gpt_replies = self.tbot.chatgpt.invokegpt_second()

               # self.gpt_replies =  self.tbot.reply_messages_v2(self.from_match_id_to_match_object(self.selected_match_id), self.current_message,self.msg_enhancement)
            else:
                self.gpt_replies = self.tbot.reply_messages_v2(self.from_match_id_to_match_object(self.selected_match_id), self.current_message,self.msg_enhancement)
        else:
            self.gpt_replies = self.tbot.generate_enhancements()
    def generate_above_text(self,query):
        keyboard = self.get_menu(self.level + 1, 0)  # Move to the next level

        if self.level == 1:
            text = self.tbot.process_messages(self.selected_match_id)
        else:
            text = self.current_message
        text_parts = [text[i:i + 4000] for i in
                      range(0, len(text), 4000)]  # Splitting into parts of 4000 characters each

        '''
        for part in text_parts:
            query.edit_message_text(text=part, reply_markup=keyboard)
        '''

        # Sending each part as a separate message
        for part in text_parts:
            query.message.reply_text(text=part)

        if self.level in odd_numbers:
            query.message.reply_text(text="A", reply_markup=keyboard)
        else:
            for idx, part in enumerate(self.gpt_message[:min(self.ITEMS_PER_PAGE, len(self.gpt_message))]):
                if idx == min((self.ITEMS_PER_PAGE - 1, len(self.gpt_message) - 1)):
                    query.message.reply_text(text=part, reply_markup=keyboard)
                else:
                    query.message.reply_text(text=part)
    def button(self, update, context) -> None:
        query = update.callback_query
        query.answer()
        data = query.data.split("_")

        if len(data) == 4 :
            self.selected_match_id = data[3]
        action = data[1]
        if (action != "no") and (action != "yes"): # CLick does not come from Yes/No confirmation
            self.level = int(data[0])
            self.page = int(data[2])

        if action == 'yes' and (self.level) in even_numbers:  # I confirm what's been done
            self.complete_action(query)
            return
        if (action == 'backlevel') :
            self.page = 0
            self.level = self.level-1
            self.act_on_page_change(query)

        if (action == 'custom') or (action == 'enhance'):
            self.invite_to_send_message(query)
            return

        if action == 'no' :
            self.act_on_page_change(query)

        if action in ["next", "prev"]: # display new Buttons
            self.act_on_page_change(query)
        else:
            # click on a relevant button
                if not(('custom' in data) or ('enhance' in data)):
                    self.act_on_click(data) #         # populate current_message or msg_enhancement
                self.generate_future_buttons_content_from_choices()
                self.generate_above_text(query)

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()