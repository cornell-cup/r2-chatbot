from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

desc: str = 'Movement Command: Any task involving moving/rotating C1C0\'s body or arms.'

def handler(api: OpenAPI, message: str) -> str:
    print('Movement Control')
