from chatterbot import ChatBot
from util import utils

import os
print(os.getcwd())

utils.set_classpath()

chatbot = ChatBot(
    "test",
    logic_adapters=[
        {
            "import_path": "logic_adapters.weather_adapter.WeatherAdapter",
            "package": "`"
        },
        {
            "import_path": "logic_adapters.restaurant_adapter.RestaurantAdapter"
        }
    ]
)


while True:
    try:
        response = chatbot.get_response(input())
        print(response)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
