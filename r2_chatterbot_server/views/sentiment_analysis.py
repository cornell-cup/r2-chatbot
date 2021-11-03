from flask import current_app, Blueprint, request
from r2_chatterbot.util import sentiment

sentiment_analysis = Blueprint('sentiment_analysis', __name__, url_prefix='/sentiment_analysis')

@sentiment_analysis.route('/', methods=['GET'])
def get_sentiment_analysis():
    if request.method == 'GET':
        speech = request.args.get('speech', '')
        sent, conf = sentiment.analyze(speech)
        print(f'Sentiment: {sent}')
        print(f'Confidence level: {conf}')
        return sent + ', ' + str(conf)
