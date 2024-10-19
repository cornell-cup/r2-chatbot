from client.audio import speech_to_text, recognize_C1C0 # Audio Interface
from client.client import OpenAPI # Client Interface

from labels.config import desc as config_desc, handler as config_handler # Configuration Specifications
from labels.general import desc as general_desc, handler as general_handler # General Info Specifications
from labels.movement import desc as movement_desc, handler as movement_handler # Movement Specifications
from labels.recognition import desc as recognition_desc, handler as recognition_handler # Recognition Specifications

from typing import Callable, Dict # Type Hinting

if __name__ == '__main__':
    # Initializing OpenAI client
    client: OpenAPI = OpenAPI()

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        config_desc:      lambda msg: config_handler(client, msg),
        # general_desc:     lambda msg: general_handler(client, msg),
        # movement_desc:    lambda msg: movement_handler(client, msg),
        recognition_desc: lambda msg: recognition_handler(client, msg)
    }

    # Infinite loop for chatbot
    while True:
        # Receiving audio from user and checking for C1C0 name
        msg: str = speech_to_text()
        print(f"\033[32mUser: {msg}\033[0m")
        if msg is None or not recognize_C1C0(msg): continue

        print("C1C0: Hey! How can I help you today?")

        # Finding and calling handler for message
        # label, score = client.categorize(msg, list(mapping.keys()))
        # if (score > LABEL_THRESHOLD): mapping[label](msg)
