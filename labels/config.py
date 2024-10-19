from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

desc: str = 'Configuration: Any task related to turning on or off C1C0\'s settings or error handling.'
subtask1: str = 'Turn off voice recognition feature of C1C0.'
subtask2: str = 'Could not understand the audio message.'
subtasks: list[str] = [subtask1, subtask2]

def handler(api: OpenAPI, message: str) -> str:
    label: str = api.categorize(message, subtasks)
    if label == subtask1: return subtask1_handler(api, message)
    if label == subtask2: return subtask2_handler(api, message)


def subtask1_handler(api: OpenAPI, message: str) -> str:
    print("Ending Chatbot Loop")
    exit(0)


def subtask2_handler(api: OpenAPI, message: str) -> str:
    print("No Audio Parsed")
