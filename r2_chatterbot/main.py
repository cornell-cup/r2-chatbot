import ast
import socket
import io
import json
import requests
from util import live_streaming
from util import nlp_util
from util import keywords
from util import make_response
from util import playtrack
from util import path_planning
from util import object_detection
from util import face_recognition
from util import utils
from util import sentiment
from util.api import weather
from util.api import restaurant
from topic_classifier import get_topic
from playsound import playsound
import re
import sys
import os
# import corpus_and_adapter
# from question_answer import get_answer
import time
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# for flask setup

USE_AWS = True

print(os.getcwd())
credential_path = "api_keys/speech_to_text.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# url = "http://18.216.143.187/"
url = "http://3.13.116.251/"
route = "chatbot_qa/"
# route = "c1c0_aws_flask/r2-chatbot/r2_chatterbot_server/"

utils.set_classpath()


def main():
    print("Hello! I am C1C0. I can answer questions and execute commands.")
    while True:
        # gets a tuple of phrase and confidence
        # answer = live_streaming.main()
        # speech = live_streaming.get_string(answer)
        # confidence = live_streaming.get_confidence(answer)
        speech = input()
        print('Question is: ' + speech)
        before = time.time()
        response = "Sorry, I don't understand"

        if "quit" in speech or "stop" in speech:
            break

        if("cico" in speech.lower() or "kiko" in speech.lower() or "c1c0" in speech.lower()) and \
                ("hey" in speech.lower()):
            # filter out cico since it messes with location detection
            question, question_type = nlp_util.is_question(speech)
            speech = utils.filter_cico(speech) + " "
            print("Question type: " + question_type)
            if not question and face_recognition.isFaceRecognition(speech):
                response = "executing facial recognition..."
                face_recognition.faceRecog(speech)
                # task is to transfer over to facial recognition client program
            elif not question and path_planning.isLocCommand(speech.lower()):
                response = path_planning.process_loc(speech.lower())
                # task is to transfer over to path planning on the system
            elif not question and object_detection.isObjCommand(speech.lower()):
                response = "Object to pick up: " + \
                    object_detection.object_parse(speech.lower())
                # task is to transfer over to object detection on the system
            else:
                if question:
                    data = keywords.get_topic(speech, parse_location=False)
                    keywords.modify_topic_data(data, parse_location=True)
                    if "name" in data.keys() and data["name"] == "weather":
                        keywords.modify_topic_data(data, parse_location=True)
                        api_data = weather.lookup_weather_today_city(
                            data["info"]["location"]["name"])
                        response = make_response.make_response_api(
                            data, api_data)
                    elif "name" in data.keys() and data["name"] == "restaurant":
                        keywords.modify_topic_data(data, parse_location=True)
                        api_data = restaurant.lookup_restaurant_city(
                            data["info"]["location"]["name"])
                        response = make_response.make_response_api(
                            data, api_data)
                    else:
                        if USE_AWS:
                            response = requests.get(
                                url+route, params={'speech': speech})
                            if response.ok:
                                response = response.text
                                # print(response)
                                response = ast.literal_eval(response)
                                answers = response['answers']
                                # for i in range(len(answers)):
                                #     print(f'Answer {i}: {answers[i]}')

                                # this is response with highest score, we need to keep all answers somewhere
                                # response = response['answers'][0]['answer']
                                response = response['answers']
                            else:
                                raise Exception('bad request')
                        else:
                            # response = get_answer(speech)
                            response = "go to question-answering"
                else:
                    sent, conf = sentiment.analyze(speech)
                    response = f"Sentiment: {sent} \t Confidence: {conf}"

            if type(response) == list:
                i = 0
                while i < len(response):
                    answer = response[i]['answer']
                    if i == 0:
                        print(
                            f'I think the answer is {answer}. Is this correct?')
                    else:
                        print(f'Ok, got it. Is the answer then {answer}?')
                    user_response = input().lower()

                    # very simple interface, we can also experiment with if the user supplies the actual answer that they want
                    # there are also times when the system actually gets multiple correct answers so we can try to find all of those if we want (i.e. Grogu/Baby Yoda)
                    if 'yes' in user_response:
                        print('Ayy we love to see it')
                        break
                    else:
                        i += 1
            else:
                print('Response: ' + response)
                after = time.time()
                print("Time: ", after - before)
            # send this element to AWS for response generation

            # begin the flask transfer now


if __name__ == '__main__':
    # playsound('sounds/cicoremix.mp3')
    main()
