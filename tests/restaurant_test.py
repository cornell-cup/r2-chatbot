import sys
sys.path.insert(1, "util")

import json
import keywords
import make_response
from api import restaurant

if __name__ == "__main__":
    restaurant.import_keys()
    with open("tests/restaurant_question_test.txt") as f:
        line = f.readline()
        topic_data = keywords.get_topic(line)
        if topic_data["name"] == "restaurant":
            lat, lng = restaurant.city_to_coord("ithaca new york")
            data = restaurant.lookup_restaurant(lat, lng)
            #print(json.dumps(data))
            print(make_response.make_response_api(topic_data, data))

