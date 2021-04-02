from flask import Flask, request
from flask_s3 import FlaskS3

s3 = FlaskS3()
config_filename = 'app.cfg'

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    s3.init_app(app)

    from views import chatbot_qa
    app.register_blueprint(chatbot_qa)

    return app


