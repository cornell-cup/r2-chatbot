from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

def handler(api: OpenAPI, message: str) -> str:
    print('Error Handler')
