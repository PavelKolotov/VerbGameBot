import logging
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from config import VK_API_KEY, PROJECT_ID, SESSION_ID, LANGUAGE_CODE, TG_BOT_API_KEY
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
    try:
        vk_session = vk.VkApi(token=VK_API_KEY)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text_answer, fallback = detect_intent_texts(PROJECT_ID, SESSION_ID, event.text, LANGUAGE_CODE)
                if fallback:
                    logger.info('Unclear question')
                else:
                    send_message(event.user_id, text_answer, vk_api)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    telegram_log_handler = TelegramLoggingHandler(TG_BOT_API_KEY, SESSION_ID)
    logging.basicConfig(
        handlers=[telegram_log_handler],
        level=logging.ERROR,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )
    main()
