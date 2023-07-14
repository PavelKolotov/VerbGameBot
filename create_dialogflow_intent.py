import argparse
import json
import logging

from google.cloud import dialogflow

from config import PROJECT_ID


def create_intent(project_id, json_path):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    with open(json_path, 'r') as file:
        questions = json.load(file)

    for question in questions:
        display_name = question
        training_phrases_parts = questions[display_name]['questions']
        message_texts = [questions[display_name]['answer']]
        training_phrases = create_training_phrases(training_phrases_parts)
        message = create_message(message_texts)

        intent = dialogflow.Intent(
            display_name=display_name, training_phrases=training_phrases, messages=[message]
        )

        try:
            response = intents_client.create_intent(
                request={'parent': parent, 'intent': intent}
            )
            logging.info(f'Intent created: {response}')
        except Exception as e:
            logging.error(f'Failed to create intent: {e}')


def create_training_phrases(training_phrases_parts):
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    return training_phrases


def create_message(message_texts):
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    return message


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json_path', help='Path to the JSON file with questions',
                        default='questions.json')
    args = parser.parse_args()
    json_path = args.json_path

    logging.basicConfig(level=logging.INFO)

    create_intent(PROJECT_ID, json_path)
