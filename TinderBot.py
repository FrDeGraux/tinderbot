from telegram_bot import TelegramBot
import datetime
import os
from tinder import TinderAPI
from dialog import Dialog
from logger import logger
from opencc import OpenCC
from dotenv import load_dotenv
from chatgpt import ChatGPTCustom
from json import JSONDecodeError


load_dotenv('.env')
cc = OpenCC('s2t')
class TinderBot(object) :
    def __init__(self) :
        self.dialog = Dialog()
        self.chatgpt = ChatGPTCustom()
        self.tinder_api = TinderAPI(os.getenv('TINDER_TOKEN'))
        try :
            self.profile = self.tinder_api.profile()
        except :
            raise Exception("Unable to log in using the current API Key")
        self.user_id = self.profile.id
        self.operations = {
            'Profile Opener': lambda x, y: self.generate_classic_opener(x, y),
            'Classic Opener': lambda x, y: self.generate_classic_opener(x, y),
            'generate_gpt_opener': lambda x, y: self.generate_gpt_opener(x, y),
        }

    def send_response(self, response, to_user_id):
        chatroom = self.tinder_api.get_messages(to_user_id)
        chatroom.send(response, self.user_id, to_user_id)

        logger.info(f' Reply: {response}')
    def get_matches_names(self):
        matches = self.get_matches()
        names = [{'name': item.person.name, 'id' : item.match_id} for item in matches]
        return names
    def get_matches(self):
        matches = self.tinder_api.matches(limit=10)
        return matches

    def process_messages(self,match_id):
        chatroom = self.tinder_api.get_messages(match_id)

        result_text = ''
        for message in chatroom.messages:
            prefix = "Me: " if message.from_id == os.getenv('MY_TINDER_ID')  else "Her: "
            result_text += prefix + message.message+ '\n'
        return result_text.strip()  # Remove the last newline character
    def has_new_message(self,in_match_id):
        chatroom = self.tinder_api.get_messages(in_match_id)
        lastest_message = chatroom.get_lastest_message()
        if lastest_message:
            if (lastest_message.from_id == (in_match_id)) :
                return True
        return False
    def is_a_new_match(self,in_match_id):
        chatroom = self.tinder_api.get_messages(in_match_id)
        lastest_message = chatroom.get_lastest_message()
        if lastest_message:
            return False
        else :
            return True
    def open_conversation(self,match):
        chatroom = self.tinder_api.get_messages(match.match_id)
        match.language = self.get_languages(match)

    def reply_messages(self):
        try:
            profile = self.tinder_api.profile()
        except (JSONDecodeError):
            raise Exception(" Token " + os.getenv('TINDER_TOKEN') + " not existing anymore")
        user_id = profile.id

        for match in self.tinder_api.matches(limit=50):
            chatroom = self.tinder_api.get_messages(match.match_id)
            lastest_message = chatroom.get_lastest_message()
            pass

            if (match.language is None):
                match.language = self.get_languages(match)
            chatroom = self.tinder_api.get_messages(match.match_id)
            lastest_message = chatroom.get_lastest_message()
            if lastest_message: # is there a new message ?
                if lastest_message.from_id == user_id:
                    from_user_id = lastest_message.from_id
                    to_user_id = lastest_message.to_id
                    last_message = 'me'
                else:
                    from_user_id = lastest_message.to_id
                    to_user_id = lastest_message.from_id
                    last_message = 'other'
                sent_date = lastest_message.sent_date
                if last_message == 'me' or (sent_date + datetime.timedelta(days=1)) < datetime.datetime.now(): # Relance après un jour
                    content = self.dialog.generate_typic_input(from_user_id, to_user_id, chatroom.messages[::-1])
                    list_responses = self.chatgpt.ask_to_gpt(content,int(os.getenv('N_ALTERNATIVES')))
                    pass
                    # Telegram
                  #  self.send_response(chatroom, response, content, from_user_id, to_user_id)

            else:
                pass
               # content = self.dialog.generate_initialize_input(user_id, match.match_id, match)
               # response = self.chatgpt.ask_to_gpt(content)
                #Telegram
              #  self.send_response(chatroom, response, content, user_id, match.match_id)
    def generate_enhancements(self):
        return Dialog.LIST_ENHANCEMENTS
    def generate_openers(self):
        return Dialog.LIST_OPENERS

    def get_languages(self,in_match):
        sBio = in_match.person.bio
        strRqst = "can you tell me in a single word the language of this text " + sBio + "If it is not speakable language, answer French"
        response = 'French'
     #   response = chatgpt.get_response(strRqst)
        return response.lower().replace('.', '')

    def generate_opener(self, in_match, in_opener):
            if in_opener not in self.operations:
                return self.generate_gpt_opener(in_match, in_opener)
            return self.operations[in_opener](in_match, in_opener)

    def generate_profile_opener(self, in_match,in_opener):
            content =  "Can you generate me a Tinder openers from the PUA " + in_opener + " technique ." + " It should be based on the following bio " + in_match.bio + "The opener should be based on " + \
                Dialog.openers_dict[in_opener] + ". The opener should be in " + self.get_languages((in_match))  + " and immediately start yout reply "

            list_responses = self.chatgpt.ask_to_gpt(content, int(os.getenv('N_ALTERNATIVES')))
            return list_responses

    def generate_classic_opener(self, in_match,in_opener):
            list_responses =  ["Hey " + in_match.person.name + " Sympa le match ; " +  "Curieux de savoir ou tu habites !"]
            return list_responses

    def generate_gpt_opener(self, in_match,in_opener):
            content =  "Can you generate me a Tinder openers based on the following bio " + in_match.person.bio + "The opener should be based on " + \
                Dialog.openers_dict[in_opener] + ". The opener should be in " + self.get_languages((in_match)) + " and immediately start yout reply "
            return self.chatgpt.invoke_openers()
            list_responses = self.chatgpt.ask_to_gpt(content, int(os.getenv('N_ALTERNATIVES')))
            return list_responses
    # 1. More classy
    def send_reply(self,chatroom,response):
        (from_user_id,to_user_id) = self.get_ids(chatroom)
        self.send_response(chatroom, response, to_user_id)

    def get_ids(self,chatroom):
        lastest_message = chatroom.get_lastest_message()
        if lastest_message:  # is there a new message ?
            if lastest_message.from_id == self.user_id:  # last message comes from me
                from_user_id = lastest_message.from_id
                to_user_id = lastest_message.to_id
                last_message = 'me'
            else:
                from_user_id = lastest_message.to_id  # last message comes from her
                to_user_id = lastest_message.from_id
        return (from_user_id,to_user_id)

    # Generate the reply message
    def reply_messages_v2(self,match,current_message,msg_enhancement = None):
    # GENERATE REPLY TO SPECIFIC MATCH
            if (match.language is None):
                match.language = self.get_languages(match)
            chatroom = self.tinder_api.get_messages(match.match_id)
            if len(chatroom.messages) == 0 :
                list_responses = self.chatgpt.enrich_by_gpt(current_message, msg_enhancement, int(os.getenv('N_ALTERNATIVES')))
                return list_responses

            lastest_message = chatroom.get_lastest_message()
            if lastest_message: # is there a new message ?
                if lastest_message.from_id == self.user_id: # last message comes from me
                    from_user_id = lastest_message.from_id
                    to_user_id = lastest_message.to_id
                    last_message = 'me'
                else:
                    from_user_id = lastest_message.to_id # last message comes from her
                    to_user_id = lastest_message.from_id
                    last_message = 'other'
                sent_date = lastest_message.sent_date
                if last_message == 'me' or ((sent_date + datetime.timedelta(days=1)) < datetime.datetime.now()): # Relance après un jour
                    content = self.dialog.generate_typic_input(from_user_id, to_user_id, chatroom.messages[::-1]) # CHATGPT CONTENT
                    list_responses = [str(i) for i in range(1,int(os.getenv('N_ALTERNATIVES'))+1)]
                    if current_message == "" :
                        list_responses = self.chatgpt.ask_to_gpt(content,int(os.getenv('N_ALTERNATIVES')))
                    else :
                        list_responses = self.chatgpt.enrich_by_gpt(current_message,msg_enhancement,int(os.getenv('N_ALTERNATIVES')))
                    return list_responses


                    # Telegram
                  #   self.send_response(chatroom, response, content, from_user_id, to_user_id)

            else: # No new message
                return None
               # content = self.dialog.generate_initialize_input(user_id, match.match_id, match)
               # response = self.chatgpt.ask_to_gpt(content)
                #Telegram
              #  self.send_response(chatroom, response, content, user_id, match.match_id
