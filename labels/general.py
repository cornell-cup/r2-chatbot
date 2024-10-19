from client.config import * # Configuration
from client.client import OpenAPI # Client Interface


desc: str = 'General: Any task related to requesting general knowledge or information.'


def handler(api: OpenAPI, message: str) -> str:
    print('General Handler Not Implemented Yet')
