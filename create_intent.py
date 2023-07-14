import argparse
import json

from google.cloud import dialogflow
from config import PROJECT_ID


def create_intent(project_id):
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json_path', help='Путь к json файлу с вопросами',
                        default='questions.json')
    args = parser.parse_args()
    json_path = args.json_path

    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    with open(f'{json_path}', 'r') as file:
        questions = json.load(file)

    for question in questions:
        display_name = question
        training_phrases_parts = questions[display_name]['questions']
        message_texts = [questions[display_name]['answer']]
        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow.Intent.Message.Text(text=message_texts)
        message = dialogflow.Intent.Message(text=text)

        intent = dialogflow.Intent(
            display_name=display_name, training_phrases=training_phrases, messages=[message]
        )

        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )

        print("Intent created: {}".format(response))


if __name__ == '__main__':
    create_intent(PROJECT_ID)