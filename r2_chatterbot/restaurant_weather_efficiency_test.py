import sys
import os
import ast
import time

sys.path.insert(1, "util")

import random
from util import keywords
import json
import requests

import json
from util import make_response
from util.api import restaurant

from util.api import weather
from util import nlp_util
from util import utils

USE_AWS = True
weather_restaurant_route = "weather_restaurant"
url = "http://3.13.116.251/"

if __name__ == "__main__":
    utils.set_classpath()
    with open("restaurant_weather_efficiency_questions.txt") as f:
        correct = 0
        i = 0
        faster = 0
        aws_faster = 0
        for line in f:
            start_time = time.time()
            topic_data = keywords.get_topic(line)
            if topic_data["name"] == "restaurant":
                data = restaurant.lookup_restaurant_city(
                    topic_data["info"]["location"]["name"]
                )
                response = make_response.make_response_api(topic_data, data)
            if topic_data["name"] == "weather":
                data = weather.lookup_weather_today_city(
                    topic_data["info"]["location"]["name"]
                )
                response = make_response.make_response_api(topic_data, data)
            end_time = time.time()
            print("--- %s seconds ---" % (end_time - start_time))
            start_time_aws = time.time()
            response = requests.get(
                url + weather_restaurant_route,
                params={"speech": line},
            )
            if response.ok:
                response = response.text
                print(response)
                # response = ast.literal_eval(response)
                # for i in range(len(answers)):
                #     print(f'Answer {i}: {answers[i]}')

                # this is response with highest score, we need to keep all answers somewhere
                # response = response['answers'][0]['answer']
                # aws_response = response["answers"][0]["answer"]
            else:
                raise Exception("bad request")
            end_time_aws = time.time()
            local_duration = end_time - start_time
            aws_duration = end_time_aws - start_time_aws
            print("local performance %s seconds" % (local_duration))
            print("aws performance %s seconds" % (aws_duration))
            if aws_duration < local_duration:
                faster = faster + (local_duration - aws_duration) / local_duration
                aws_faster = aws_faster + 1

            if response.strip() == response.strip():
                correct += 1
            i += 1
        print("it has " + "{:.2f}".format(correct / i * 100) + " percent accuracy")

        print(
            "aws is better than local by "
            + "{:.2f}".format(aws_faster / i * 100)
            + " percent of the time "
        )
        if aws_faster != 0:
            print(
                "aws is better than local by "
                + "{:.2f}".format(faster / aws_faster * 100)
                + " percent"
            )
