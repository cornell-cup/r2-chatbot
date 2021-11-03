from flask import current_app, Blueprint, request
from r2_chatterbot.question_answer import get_answer
chatbot_qa = Blueprint('chatbot_qa', __name__, url_prefix='/chatbot_qa')

@chatbot_qa.route('/', methods=['GET'])
def get_qa():
    if request.method == 'GET':
        print(f'\nRequest args: {request.args}\n')
        speech = request.args.get('speech', '')
        print(f'\nSpeech: {speech}\n')
        answer = get_answer(speech)
        print(f'\nAnswer: {answer}\n')
        return answer
