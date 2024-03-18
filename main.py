from telegram_bot import TelegramBot
import datetime
import os
from models import OpenAIModel
from tinder import TinderAPI
from dialog import Dialog
from logger import logger
from opencc import OpenCC
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from fastapi import FastAPI
'''
load_dotenv('.env')

models = OpenAIModel(api_key=os.getenv('OPENAI_API'), model_engine=os.getenv('OPENAI_MODEL_ENGINE'))

chatgpt = ChatGPT(models)
chatgpt.get_response("Say hallow")
pass
dalle = DALLE(models)
dialog = Dialog()

scheduler = AsyncIOScheduler()
cc = OpenCC('s2t')
TINDER_TOKEN = os.getenv('TINDER_TOKEN')
#objTelBot = TelegramBot()

def get_languages(in_match) :
    sBio = in_match.bio
    sBio = '💼: 👩‍🔬+ 🍦+ 🐎'
    strRqst = "can you tell me in a single word the language of this text " + sBio + "If it is not speakable language, answer English"
    response = chatgpt.get_response(strRqst)
    return  response.lower().replace('.','')

def send_response(chatroom,response,content,from_user_id, to_user_id) :
    if response:
        response = cc.convert(response)
        if response.startswith('[Sender]'):
            chatroom.send(response[8:], from_user_id, to_user_id)
        else:
            chatroom.send(response, from_user_id, to_user_id)
        logger.info(f'Content: {content}, Reply: {response}')


def reply_messages():
    tinder_api = TinderAPI(TINDER_TOKEN)
    profile = tinder_api.profile()

    user_id = profile.id

    for match in tinder_api.matches(limit=50):
        if (match.language is None) :
            match.language  = get_languages(match)
        chatroom = tinder_api.get_messages(match.match_id)
        lastest_message = chatroom.get_lastest_message()
        if lastest_message:
            if lastest_message.from_id == user_id:
                from_user_id = lastest_message.from_id
                to_user_id = lastest_message.to_id
                last_message = 'me'
            else:
                from_user_id = lastest_message.to_id
                to_user_id = lastest_message.from_id
                last_message = 'other'
            sent_date = lastest_message.sent_date
            if last_message == 'other' or (sent_date + datetime.timedelta(days=1)) < datetime.datetime.now():
                content = dialog.generate_typic_input(from_user_id, to_user_id, chatroom.messages[::-1])
                response = chatgpt.get_response(content)
                send_response(chatroom,response,content,from_user_id,to_user_id)

        else :
            content = dialog.generate_initialize_input(user_id, match.match_id,match)
            response = chatgpt.get_response(content)
            send_response(chatroom, response, content, user_id, match.match_id)

async def startup():
    scheduler.start()


async def shutdown():
    scheduler.remove_job('reply_messages')


async def root():
    return {"message": "Hello World"}
'''



