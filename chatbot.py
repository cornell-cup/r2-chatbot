# import speech_recognition as sr, pyttsx3 # Default Python Libraries

from client.client import OpenAPI # Client Interface

from labels.error import handler as error_handler # Error Specifications
from labels.general import desc as general_desc, handler as general_handler # General Specifications
from labels.movement import desc as movement_desc, handler as movement_handler # Movement Specifications
from labels.recognition import desc as recognition_desc, handler as recognition_handler # Recognition Specifications

from typing import Callable, Dict # Type Hinting

if __name__ == '__main__':
    # Initializing OpenAI client
    client: OpenAPI = OpenAPI()

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        general_desc:     lambda msg: general_handler(client, msg),
        movement_desc:    lambda msg: movement_handler(client, msg),
        recognition_desc: lambda msg: recognition_handler(client, msg)
    }

    # try:
    #     with sr.Microphone() as source2:
    #         sr.adjust_for_ambient_noise(source2, duration=0.2)
    #         audio2 = sr.listen(source2)

    #         # Using google to recognize audio
    #         text = sr.recognize_google(audio2).lower()

    #         print("Did you say ", text)

    # except sr.RequestError as e:
    #     print("Could not request results; {0}".format(e))

    # except sr.UnknownValueError:
    #     print("unknown error occurred")

    # Infinite loop for chatbot
    while True:
        # Receiving message from user
        msg: str = input('You: ')

        # Quitting chatbot if exit command
        if msg == 'exit' or msg == 'quit': break

        # Finding and calling handler for message
        label: str = client.categorize(msg, list(mapping.keys()))
        mapping.setdefault(label, lambda msg: error_handler(client, msg))
        print(mapping[label](msg))
