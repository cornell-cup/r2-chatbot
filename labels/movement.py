from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

desc: str     = 'Movement Command: Any task involving moving/rotating C1C0\'s body or arms.'
subtask1: str = 'Move C1C0\'s body forward/backward/left/right.'
subtask2: str = 'Move C1C0\'s strong arm up/down/left/right.'
subtask3: str = 'Move C1C0\'s precise arm up/down/left/right.'
subtask4: str = 'Make C1C0\'s head rotate left/right.'

def handler(api: OpenAPI, message: str) -> str:
    label: str = api.categorize(message, [subtask1, subtask2, subtask3, subtask4])
    if label == subtask1: return 'movement_get: locomotion', 'movement_put: locomotion'
    if label == subtask2: return 'movement_get: strong_arm', 'movement_put: strong_arm'
    if label == subtask3: return 'movement_get: precise_arm', 'movement_put: precise_arm'
    if label == subtask4: return 'movement_get: rotate', 'movement_put: rotate'
    return 'null', 'null' # Error Handling
