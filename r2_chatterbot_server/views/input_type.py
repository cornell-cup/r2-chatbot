from flask import current_app, Blueprint, request

import sys
sys.path.insert(0,'/home/ec2-user/c1c0_aws_flask/r2-chatbot/r2_chatterbot')

from util import input_type

input_type = Blueprint('input_type', __name__, url_prefix='/input_type')

@input_type.route('/', methods=['GET'])
def get_input_type():
    if request.method == 'GET':
        speech = request.args.get('speech', '')
        response = input_type.getInputType(speech)
        return response
