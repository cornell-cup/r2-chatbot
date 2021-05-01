import ast
import socket
import io
import json
import requests
import pandas as pd
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
import random
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

# saved answers setup
if os.path.exists('./saved_answers.csv'):
    saved_answers = pd.read_csv('./saved_answers.csv').to_dict()
else:
    saved_answers = {}

# bad punctuation for cleaning string (no question mark)
punctuations = '''!()-[]{};:'"\,<>./@#$%^&*_~'''


def no_punct(string):
    no_punct = ''
    for char in string:
        if char not in punctuations:
            no_punct += char

    no_punct = no_punct.strip()
    return no_puct


def main():
    print("Hello! I am C1C0. I can answer questions and execute commands.")
    while True:
        # gets a tuple of phrase and confidence
        answer = live_streaming.main()
        speech = live_streaming.get_string(answer)
        confidence = live_streaming.get_confidence(answer)
        # speech = input()
        print(speech)
        before = time.time()
        response = "Sorry, I don't understand"

        if "quit" in speech.lower() or "stop" in speech.lower():
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
            elif (not question or question_type == "yes/no question") and object_detection.isObjCommand(speech.lower()):
                pick_up = object_detection.object_parse(speech.lower())
                if pick_up:
                    response = "Object to pick up: " + pick_up
                else:
                    response = "Sorry, I can't recognize this object."
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
                        # Q/A section

                        # check if question in saved answers (if, so we don't need to go to AWS)
                        clean_q = no_punct(speech)
                        if clean_q in saved_answers:
                            # choose random answer (all are guaranteed correct if they're here)
                            all_good_answers = []
                            idx = random.randint(0, len(all_good_answers))
                            response = all_good_answers[idx]
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
                    if 'yes' in user_response or 'yeah' in user_response:
                        # save question/answer pair
                        clean_q = no_punct(speech)
                        saved_answers[clean_q] = [answer]

                        print('Ayy we love to see it. Any others that I should know?')

                        # assumes response is just answers, no other small talk
                        new_words = input().split(', ')
                        saved_answers[clean_q] += new_words
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

    # need to save the new saved_answers thing into a csv
    import csv
    save_file = open('./saved_answers.csv', 'w+')
    writer = csv.writer(save_file)

    for key, value in saved_answers.items():
        writer.writerow([key, value])

    save_file.close()
