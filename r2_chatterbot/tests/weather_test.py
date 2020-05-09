import sys
import os
sys.path.insert(1, "util")

import random

import json
import keywords
import make_response
from api import weather
from util import nlp_util
from util import utils

cico = ["cico", "kiko", "c1c0", "k1k0", "Cico", "C1c0", "K1k0"]

if __name__ == "__main__":
    utils.set_classpath()
    with open("tests/weather_and_places.txt") as f:
    #with open("tests/weather_question_tests.txt") as f:
        for line in f:
            
            if random.random() < .5:
                line = cico[random.randint(0, len(cico)-1)] + " " + line

            print(line)
            line = utils.filter_cico(line)
            print(line.strip())
            
            topic_data = keywords.get_topic(line)
            if topic_data["name"] == "weather":
                '''
                data = None
                if "location" in topic_data["info"]:
                    data = weather.lookup_weather_today_city(topic_data["info"]["location"])
                else:
                    data = weather.lookup_weather_today_city("ithaca new york")
                '''
                data = weather.lookup_weather_today_city(topic_data["info"]["location"]["name"])
                
                #print(json.dumps(data))
                print(make_response.make_response_api(topic_data, data))
                print()



