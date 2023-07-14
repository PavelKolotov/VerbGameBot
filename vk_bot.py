import logging
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from config import VK_API_KEY, PROJECT_ID, SESSION_ID, LANGUAGE_CODE
from tg_bot import detect_intent_texts


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
logger = logging.getLogger(__name__)


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
                text_answer = detect_intent_texts(PROJECT_ID, SESSION_ID, event.text, LANGUAGE_CODE)
                send_message(event.user_id, text_answer, vk_api)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
