import logging
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import dialogflow_v2beta1 as dialogflow

from config import VK_API_KEY, PROJECT_ID, SESSION_ID, LANGUAGE_CODE


logger = logging.getLogger(__name__)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


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
                if not text_answer:
                    logger.info('Unclear question')
                else:
                    send_message(event.user_id, text_answer, vk_api)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    main()
