import logging

from environs import Env
import telebot

from telegram_handler import TelegramLoggingHandler
from dialogflow_api import detect_intent_texts


logger = logging.getLogger('TG_BOT')


if __name__ == '__main__':

    env = Env()
    env.read_env()
    tg_bot_api_key = env.str('TG_BOT_API_KEY')
    project_id = env.str('PROJECT_ID')
    language_code = env.str('LANGUAGE_CODE')
    tg_id = env.int('TG_ID')
    bot = telebot.TeleBot(tg_bot_api_key)
    telegram_log_handler = TelegramLoggingHandler(tg_bot_api_key, tg_id)
    logging.basicConfig(
        handlers=[telegram_log_handler],
        level=logging.ERROR,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )


    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.reply_to(message, f'Здравствуйте {message.from_user.first_name}!')


    @bot.message_handler()
    def handle_message(message):
        try:
            session_id = f'tg-{message.chat.id}'
            answer, fallback = detect_intent_texts(project_id, session_id, message.text, language_code)
            bot.send_message(message.chat.id, answer)
        except Exception as e:
            logger.error(e)


    bot.polling()
