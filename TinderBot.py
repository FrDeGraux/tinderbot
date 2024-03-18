from telegram_bot import TelegramBot
import datetime
import os
from tinder import TinderAPI
from dialog import Dialog
from logger import logger
from opencc import OpenCC
from dotenv import load_dotenv
from fastapi import FastAPI
from chatgpt import ChatGPTCustom
from json import JSONDecodeError


load_dotenv('.env')
cc = OpenCC('s2t')
class TinderBot(object) :
    def __init__(self) :
        self.dialog = Dialog()
        self.chatgpt = ChatGPTCustom()
        self.tinder_api = TinderAPI(os.getenv('TINDER_TOKEN'))

        pass
    def get_languages(self,in_match):
        sBio = in_match.person.bio
        strRqst = "can you tell me in a single word the language of this text " + sBio + "If it is not speakable language, answer French"
        response = 'French'
     #   response = chatgpt.get_response(strRqst)
        return response.lower().replace('.', '')
    def send_response(self,chatroom, response, content, from_user_id, to_user_id):
        if response:
            response = cc.convert(response)
            if response.startswith('[Sender]'):
                chatroom.send(response[8:], from_user_id, to_user_id)
            else:
                chatroom.send(response, from_user_id, to_user_id)
            logger.info(f'Content: {content}, Reply: {response}')

    def reply_messages(self):
        try :
            profile = self.tinder_api.profile()
        except (JSONDecodeError) :
            raise Exception(" Token "  + os.getenv('TINDER_TOKEN') + " not existing anymore")
        user_id = profile.id

        for match in self.tinder_api.matches(limit=50):
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
                if last_message == 'other' or (sent_date + datetime.timedelta(days=1)) < datetime.datetime.now(): # Relance après un jour
                    content = self.dialog.generate_typic_input(from_user_id, to_user_id, chatroom.messages[::-1])
                    list_responses = self.chatgpt.ask_to_gpt(content,int(os.getenv('N_ALTERNATIVES')))
                    pass
                    # Telegram
                    #self.send_response(chatroom, response, content, from_user_id, to_user_id)

            else:
                content = self.dialog.generate_initialize_input(user_id, match.match_id, match)
                response = self.chatgpt.ask_to_gpt(content)
                #Telegram
                self.send_response(chatroom, response, content, user_id, match.match_id)
