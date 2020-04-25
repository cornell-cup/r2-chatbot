import sys
import os
sys.path.insert(1, "util")

import json
import keywords
import make_response
from api import restaurant



if __name__ == "__main__":
    if "CLASSPATH" not in os.environ:
        os.environ["CLASSPATH"] = ""
    os.environ["CLASSPATH"] += (":%s/dep/stanford-ner/stanford-ner.jar"%(os.getcwd()))
    print(os.environ["CLASSPATH"])

    #with open("tests/restaurant_question_test.txt") as f:
    with open("tests/restaurant_and_places.txt") as f:
        for line in f:
            print("\n question is:")
            print(line)
            topic_data = keywords.get_topic(line)
            if topic_data["name"] == "restaurant":
                data = restaurant.lookup_restaurant_city(topic_data["info"]["location"]["name"])
                #print(json.dumps(data))
                print(make_response.make_response_api(topic_data, data))

