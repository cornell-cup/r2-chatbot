'''
This file contains functionality to generate chatbot responses to user
input
'''

import sys
sys.path.insert(1, "util")

from api import weather

def make_response_api(topic_data, api_data):
    response = ""
    if topic_data["name"] == "weather":
        if "temperature" in topic_data["info"]:
            
            pass
        response = "There is %s"%(api_data["weather"][0]["description"])

    return response

