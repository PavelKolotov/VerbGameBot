import telebot
import logging


from environs import Env
from google.cloud import dialogflow_v2beta1 as dialogflow


env = Env()
env.read_env()

project_id = env.str('PROJECT_ID')
suffix = env.str('SUFFIX')
session_id = env.int('SESSION_ID')
language_code = env.str('LANGUAGE_CODE')
tg_bot_api_key = env.str('TG_BOT_API_KEY')

bot = telebot.TeleBot(tg_bot_api_key)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, f'Здравствуйте {message.from_user.first_name}!')


@bot.message_handler()
def handle_message(message):
    text = detect_intent_texts(project_id, session_id, message.text, language_code)
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':

    bot.polling()

