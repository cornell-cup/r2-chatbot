from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications


desc: str     = 'Movement: Any task involving moving/rotating C1C0\'s body or arms.'
subtask1: str = 'Move C1C0\'s body forward/backward/left/right.'
subtask2: str = 'Move C1C0\'s strong arm up/down/left/right.'
subtask3: str = 'Move C1C0\'s precise arm up/down/left/right.'
subtask4: str = 'Make C1C0\'s head rotate left/right/reset.'
subtasks: list[str] = [subtask1, subtask2, subtask3, subtask4]


def handler(api: OpenAPI, message: str) -> str:
    label: str = api.categorize(message, subtasks)
    if label == subtask1: return subtask1_handler(api, message)
    if label == subtask2: return subtask2_handler(api, message)
    if label == subtask3: return subtask3_handler(api, message)
    if label == subtask4: return subtask4_handler(api, message)
    return config_handler(api, message)


def subtask1_handler(api: OpenAPI, message: str) -> str:
    return print('movement_put: locomotion')


def subtask2_handler(api: OpenAPI, message: str) -> str:
    return print('movement_put: strong_arm')


def subtask3_handler(api: OpenAPI, message: str) -> str:
    return print('movement_put: precise_arm')


def subtask4_handler(api: OpenAPI, message: str) -> str:
    return print('movement_put: rotate')
