import telebot

from environs import Env

env = Env()
env.read_env()

tg_bot_api_key = env.str('TG_BOT_API_KEY')
bot = telebot.TeleBot(tg_bot_api_key)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Привет! Я бот.')


@bot.message_handler()
def handle_message(message):
    bot.send_message(message.chat.id, message.text)


bot.polling()

