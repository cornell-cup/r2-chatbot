import ast
import socket
import io
import json
import requests
import pandas as pd
from util import client
from util import live_streaming
from util import nlp_util
from util import keywords
from util import make_response

# from util import playtrack
from util import path_planning
from util import object_detection
from util import face_recognition
from util import utils
from util import sentiment
from util.api import weather
from util.api import restaurant
from util import command_type
from util.sound_engine import SoundEngine

# from topic_classifier import get_topic
from playsound import playsound
import re
import sys
import os
import threading

# import corpus_and_adapter
# from question_answer import get_answer
import time
import nltk
import random

nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")

# for flask setup

USE_AWS = True

print(os.getcwd())
credential_path = "api_keys/speech_to_text.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

# url = "http://18.216.143.187/"
# url = "http://3.13.116.251/"
url = "http://128.253.46.196:5000/"
chatbot_qa_route = "chatbot_qa/"
sentiment_qa_route = "sentiment_analysis/"
weather_restaurant_route = "weather_restaurant"
command_type_route = "command_type"
# route = "c1c0_aws_flask/r2-chatbot/r2_chatterbot_server/"

utils.set_classpath()

# saved answers setup
if os.path.exists("./saved_answers.csv"):
    saved_answers = pd.read_csv("./saved_answers.csv").to_dict()
else:
    saved_answers = {}

# bad punctuation for cleaning string (no question mark)
punctuations = """!()-[]{};:'"\,<>./@#$%^&*_~"""



def no_punct(string):
    no_punct = ""
    for char in string:
        if char not in punctuations:
            no_punct += char

    no_punct = no_punct.strip()
    return no_punct

def main():
    sound_engine = SoundEngine(folder = os.path.join(os.getcwd(), 'sounds', 'chirp_parts'))
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
        if no_punct(speech.lower().strip(' ')) in ["quit", "stop"]:
            scheduler.close()
            break

        if ("cico" in speech.lower() or "kiko" in speech.lower() or "c1c0" in speech.lower()) and ("hey" in speech.lower()):
            # filter out cico since it messes with location detection
            question, question_type = nlp_util.is_question(speech)
            speech = utils.filter_cico(speech) + " "
            print("Question type: " + question_type)
            # uncomment this once the route is up to date on the base station
            # if USE_AWS:
                # com_type = requests.get(url + command_type_route, params={"speech": speech}).text
            # else:
            com_type = command_type.getCommandType(speech, question, question_type)
            print("Command type: " + com_type)
            if com_type == 'facial recognition':
                response = face_recognition.faceRecog(speech)
                # task is to transfer over to facial recognition client program
            elif com_type == 'path planning':
                response = path_planning.process_loc(speech.lower())
                # task is to transfer over to path planning on the system
                scheduler.communicate("path-planning" + ' ' + str(response))
            elif com_type == 'object detection':
                pick_up = object_detection.object_parse(speech.lower())
                if pick_up:
                    response = "Object to pick up: " + pick_up
                    # task is to transfer over to object detection on the system
                    scheduler.communicate("object-detection" + ' ' + response)
                else:
                    response = "Sorry, I can't recognize this object."
            else:
                if question:
                    print("C1C0 is thinking...")
                    data = keywords.get_topic(speech, parse_location=False)
                    if "name" in data.keys() and (
                        data["name"] == "weather" or data["name"] == "restaurant"
                    ):
                        if USE_AWS:
                            response = requests.get(
                                url + weather_restaurant_route,
                                params={"speech": speech},
                            )
                            if response.ok:
                                response = response.text
                            else:
                                response = "Bad request"
                        elif data["name"] == "weather":
                            keywords.modify_topic_data(data, parse_location=True)
                            api_data = weather.lookup_weather_today_city(
                                data["info"]["location"]["name"]
                            )
                            response = make_response.make_response_api(data, api_data)
                        elif data["name"] == "restaurant":
                            keywords.modify_topic_data(data, parse_location=True)
                            api_data = restaurant.lookup_restaurant_city(
                                data["info"]["location"]["name"]
                            )
                            response = make_response.make_response_api(data, api_data)
                    else:
                        # Q/A section
                        if USE_AWS:
                            response = requests.get(
                                url + chatbot_qa_route, params={"speech": speech}
                            )
                            if response.ok:
                                response = response.text
                                # print(response)
                                response = ast.literal_eval(response)
                                answers = response["answers"][0]["answer"]
                                # for i in range(len(answers)):
                                #     print(f'Answer {i}: {answers[i]}')

                                # this is response with highest score, we need to keep all answers somewhere
                                # response = response['answers'][0]['answer']
                                response = response["answers"][0]["answer"]
                            else:
                                response = "Bad request"
                        else:
                            response = "Sorry, I can't answer this right now."
                        if type(response) == list:
                            i = 0
                            while i < len(response):
                                answer = response[i]['answer']
                                if i == 0:
                                    print(
                                        f'I think the answer is {answer}. Is this correct?')
                                else:
                                    print(f'Ok, got it. Is the answer then {answer}?')
                                user_response = live_streaming.main()
                                user_response = live_streaming.get_string(user_response)
                                user_response = user_response.lower()
                                print(user_response)
                                if 'yes' in user_response or 'yeah' in user_response:
                                    break
                else:
                    response = sentiment.get_sentiment(speech, USE_AWS)

            after = time.time()
            print("Time: ", after - before)

            print('Response: ', response)
            if response == "That's great!":
                playsound('sounds/positive_r2/' + random.choice(os.listdir('sounds/positive_r2')), block = False)
            elif response == "Okay.":
                playsound('sounds/neutral_r2/' + random.choice(os.listdir('sounds/neutral_r2')), block = False)
            elif response == "That isn't good.":
                playsound('sounds/negative_r2/' + random.choice(os.listdir('sounds/negative_r2')), block = False)
            else:
                max_len = min(2, len(response))
                response = ''.join(c for c in response[:max_len] if c.isalnum())
                threading.Thread(target = sound_engine.play_text, args = [response]).start()


if __name__ == "__main__":
    playsound('sounds/cicoremix.mp3')
    scheduler = client.Client("Chatbot")
    try:
        scheduler.handshake()
    except:
        print("Scheduler handshake unsuccesful")
    try:
        main()
    except Exception as e:
        print(e)
        scheduler.close()
        sys.exit(0)

    # need to save the new saved_answers thing into a csv
    # import csv
    # save_file = open('./saved_answers.csv', 'w+')
    # writer = csv.writer(save_file)

    # for key, value in saved_answers.items():
    #     writer.writerow([key, value])

    # save_file.close()
