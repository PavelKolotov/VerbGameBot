import logging

import telebot

from config import TG_BOT_API_KEY, PROJECT_ID, SESSION_ID, LANGUAGE_CODE
from telegram_handler import TelegramLoggingHandler
from dialogflow_api import detect_intent_texts

logger = logging.getLogger('TG_BOT')

bot = telebot.TeleBot(TG_BOT_API_KEY)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, f'Здравствуйте {message.from_user.first_name}!')


@bot.message_handler()
def handle_message(message):
    try:
        answer, fallback = detect_intent_texts(PROJECT_ID, SESSION_ID, message.text, LANGUAGE_CODE)
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    telegram_log_handler = TelegramLoggingHandler(TG_BOT_API_KEY, SESSION_ID)
    logging.basicConfig(
        handlers=[telegram_log_handler],
        level=logging.ERROR,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )
    bot.polling()
