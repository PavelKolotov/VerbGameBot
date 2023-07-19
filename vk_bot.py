import logging
import random

from environs import Env

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_api import detect_intent_texts
from telegram_handler import TelegramLoggingHandler


logger = logging.getLogger('VK_BOT')


def send_message(user_id, message, vk_api):
    try:
        vk_api.messages.send(
            user_id=user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )
    except Exception as e:
        logger.error(e)


def main():
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    session_id = f'vk-{env.str("VK_ID")}'
    tg_id = env.int('TG_ID')
    language_code = env.str('LANGUAGE_CODE')
    tg_bot_api_key = env.str('TG_BOT_API_KEY')
    vk_api_key = env.str('VK_API_KEY')

    telegram_log_handler = TelegramLoggingHandler(tg_bot_api_key, tg_id)
    logging.basicConfig(
        handlers=[telegram_log_handler],
        level=logging.ERROR,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )

    try:
        vk_session = vk.VkApi(token=vk_api_key)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text_answer, fallback = detect_intent_texts(
                    project_id,
                    session_id,
                    event.text,
                    language_code
                )
                if fallback:
                    logger.info('Unclear question')
                else:
                    send_message(event.user_id, text_answer, vk_api)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":

    main()