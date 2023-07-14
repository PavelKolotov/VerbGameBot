import logging

import telebot
from google.cloud import dialogflow_v2beta1 as dialogflow

from config import TG_BOT_API_KEY, PROJECT_ID, SESSION_ID, LANGUAGE_CODE


logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TG_BOT_API_KEY)


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
    try:
        text = detect_intent_texts(PROJECT_ID, SESSION_ID, message.text, LANGUAGE_CODE)
        bot.send_message(message.chat.id, text)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    bot.polling()
