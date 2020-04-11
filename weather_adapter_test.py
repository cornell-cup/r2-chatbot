from chatterbot import ChatBot

import os
print(os.getcwd())

chatbot = ChatBot(
    "test",
    logic_adapters=[
        {
            "import_path": "logic_adapters.weather_adapter.WeatherAdapter",
            "package": "`"
        }
    ]
)


while True:
    try:
        response = chatbot.get_response(input())
        print(response)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
