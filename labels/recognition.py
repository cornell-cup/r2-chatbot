from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications


desc: str     = 'Facial Recognition: Any task involving C1C0 identifying/learning a person\'s face.'
subtask1: str = 'Recognize a person\'s face and say their name.'
subtask2: str = 'Learn a person\'s face and save their name.'
subtasks: list[str] = [subtask1, subtask2]


def handler(api: OpenAPI, message: str) -> str:
    label: str = api.categorize(message, subtasks)
    if label == subtask1: return subtask1_handler(api, message)
    if label == subtask2: return subtask2_handler(api, message)
    return config_handler(api, message)


def subtask1_handler(api: OpenAPI, message: str) -> str:
    return print('facial_get: attendance')


def subtask2_handler(api: OpenAPI, message: str) -> str:
    return print('facial_put: learn')
