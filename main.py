from util import live_streaming
from util import detect_question
from util import keywords
from util import make_response
from util import playtrack
from util.api import weather
from playsound import playsound
import re
import sys
import os

credential_path = "api_keys/Speech to Text-bef030531cd1.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def main():
    #live_streaming.delete_file()
    weather.import_keys()
    while True:
        answer = live_streaming.main()
        speech = live_streaming.get_string(answer)
        confidence = live_streaming.get_confidence(answer)
        if speech == "quit":
            break
        print(answer)
        playsound('/sounds/cicoremix.mp3')
        topic = keywords.get_topic(speech)
        if topic["name"] == "weather":
            weather_data = weather.lookup_weather_today_city(
                    "ithaca new york")
            print(weather_data)
            response = make_response.make_response_api(topic, weather_data)
            print(response)

if __name__ == '__main__':
    print('ok')
    playsound('sounds/cicoremix.mp3')
    print('ok')
    #main()
