'''
This file contains functionality to generate chatbot responses to user
input
'''

import sys
sys.path.insert(1, "util")

# util.
from api import weather
from api import restaurant

# util
import keywords

def make_response_api(topic_data, api_data):
    response = ""
    if topic_data["name"] == "weather":
        if "temperature" in topic_data["info"]["keywords"]:
            response = "It is %s degrees"%(round(api_data["main"]["temp"]))
        else:
            response = "There is %s"%(api_data["weather"][0]["description"])

    elif topic_data["name"] == "restaurant":
        list_of_restaurants = ""
        for restaurant in api_data['nearby_restaurants']:
            r = restaurant['restaurant']["name"] + ", "
            list_of_restaurants = list_of_restaurants+r
        top_choices = api_data['popularity']['top_cuisines']
        top_cuisines = "This place is famous place for "
        for t_c in top_choices:
            top_cuisines+=t_c+", "
        top_cuisines+="."
        response= top_cuisines +"The recommended restaurants are "+ list_of_restaurants

    return response

if __name__ == "__main__":
    weather.import_keys()

    with open("./tests/weather_question_tests.txt") as f:
        total = 0
        passed = 0
        for line in f:
            total += 1
            print(line)
            topic = keywords.get_topic(line)
            if topic["name"] == "weather":
                weather_data = weather.lookup_weather_today_city(
                        "xian shaanxi")
                #print(weather_data)
                response = make_response_api(topic, weather_data)
                print(response)
                passed += 1
            if topic["name"] == "restaurant":
                restaurant_data = restaurant.lookup_restaurant_city(
                        "xian shaanxi")
                print(restaurant_data)
                response = make_response_api(topic, restaurant_data)
                print(response)

    print("passed %d/%d"%(passed, total))
