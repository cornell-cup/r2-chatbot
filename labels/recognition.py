from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

desc: str     = 'Facial Recognition Command: Any task involving C1C0 identifying/learning a person\'s face.'
subtask1: str = 'Recognize a person\'s face.'
subtask2: str = 'Learn a person\'s face.'

def handler(api: OpenAPI, message: str) -> str:
    label: str = api.categorize(message, [subtask1, subtask2])
    if label == subtask1: return 'facial_get: attendance', 'facial_put: null'
    if label == subtask2: return 'facial_get: learn', 'facial_put: null'
    return 'null', 'null' # Error Handling
