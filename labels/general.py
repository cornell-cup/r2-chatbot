from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

desc: str = 'General Information: Any task that does not fit into the other categories.'

def handler(api: OpenAPI, message: str) -> str:
    print('General Handler')
