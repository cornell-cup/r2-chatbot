from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from util import utils

utils.set_classpath()

# Uncomment the following lines to enable verbose logging
import logging
logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'logic_adapters.weather_adapter.WeatherAdapter',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.db',
    read_only = True
)

corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train('chatterbot.corpus.english.greetings', "./custom_corpus.yaml")

print('Type something to begin...')

# The following loop will execute each time the user enters input
while True:
    try:
        user_input = input()
        bot_response = bot.get_response(user_input)
        print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
