from flask import current_app, Blueprint, request

import sys
#sys.path += ['/home/ec2-user/c1c0_aws_flask/r2-chatbot/r2_chatterbot']#, '/home/ec2-user/c1c0_aws_flask/r2-chatbot/r2_chatterbot/util']
sys.path.insert(0,'/home/systemslab/Desktop/chatbot/r2-chatbot/r2_chatterbot')

# import os
# os.chdir("/home/ec2-user/c1c0_aws_flask/r2-chatbot/r2_chatterbot")

from util import keywords
from util import make_response
from util.api import weather
from util.api import restaurant

#from r2_chatterbot.util import sentiment
#from r2_chatterbot import topic_classifier 
#from r2_chatterbot.util import keywords
#from r2_chatterbot.util import make_response

#from r2_chatterbot.util.api import weather
#from r2_chatterbot.util.api import restaurant



weather_restaurant = Blueprint('weather_restaurant', __name__, url_prefix='/weather_restaurant')

@weather_restaurant.route('/', methods=['GET'])
def get_sentiment_analysis():
    if request.method == 'GET':
        speech = request.args.get('speech', '')
        # sent, conf = sentiment.analyze(speech)
        # print(f'Sentiment: {sent}')
        # print(f'Confidence level: {conf}')
        print("SPEECH: ", speech)
        data = keywords.get_topic(speech, parse_location=False)
        print(data)
        keywords.modify_topic_data(data, parse_location=True)
        print(data)
        response = "TEST"
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


        return response
