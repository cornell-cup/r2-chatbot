import sys
sys.path.insert(1, "util")

import json
import keywords
import make_response
from api import weather

if __name__ == "__main__":
    weather.import_keys()
    
    with open("tests/question_keyword_tests.txt") as f:
        line = f.readline()
        topic_data = keywords.get_topic(line)
        if topic_data["name"] == "weather":
            lat, lng = weather.city_to_coord("ithaca new york")
            data = weather.lookup_weather_today(lat, lng)
            #print(json.dumps(data))
            print(make_response.make_response_api(topic_data, data))

