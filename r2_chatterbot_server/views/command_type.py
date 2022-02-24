from flask import current_app, Blueprint, request

import sys
sys.path.insert(0,'/home/ec2-user/c1c0_aws_flask/r2-chatbot/r2_chatterbot')

from util import command_type

input_type = Blueprint('command_type', __name__, url_prefix='/command_type')

@command_type.route('/', methods=['GET'])
def is_command():
    if request.method == 'GET':
        speech = request.args.get('speech', '')
        response = command_type.getCommandType(speech)
        return response
