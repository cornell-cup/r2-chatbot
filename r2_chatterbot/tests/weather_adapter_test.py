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
        line = input()
        line = utils.filter_cico(line)
        response = chatbot.get_response(line)
        print(response)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
