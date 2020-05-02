from chatterbot import ChatBot

import os
print(os.getcwd())

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
