from speech-to-text import live_streaming
from util import detect_question
from util import keywords
from util import make_response

def main():
    while True:
        answer = live_streaming.main()
        speech = live_streaming.get_string(answer)
        confidence = live_streaming.get_confidence(answer)
        if speech == "quit":
            break
        print(speech)
        
        topic = keywords.get_topic(speech)
        if topic["name"] == "weather":
            weather_data = weather.lookup_weather_today_city(
                    "ithaca new york")
            print(weather_data)
            response = make_response_api(topic, weather_data)
            print(response)

if __name__ == '__main__':
    main()

