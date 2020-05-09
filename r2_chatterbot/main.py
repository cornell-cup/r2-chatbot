from util import live_streaming
from util import nlp_util
from util import keywords
from util import make_response
from util import playtrack
from util import path_planning
from util import object_detection
from util import face_recognition
from util import utils
from util.api import weather
from util.api import restaurant
from playsound import playsound
import re
import sys
import os
import corpus_and_adapter
import re

print(os.getcwd())
credential_path = "api_keys/speech_to_text.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

utils.set_classpath()

def main():
    while True:
        #gets a tuple of phrase and confidence
        answer = live_streaming.main()
        speech = live_streaming.get_string(answer)
        confidence = live_streaming.get_confidence(answer)
        print(speech)
        if "quit" in speech or "stop" in speech:
            break
        if("cico" in speech.lower() or "kiko" in speech.lower() or "c1c0" in speech.lower()):
            # filter out cico since it messes with location detection
            speech = utils.filter_cico(speech)

            if face_recognition.isFaceRecognition(speech):
                print(face_recognition.faceRecog(speech))
            elif path_planning.isLocCommand(speech.lower()):
                print("Move command (itemMove, direction, moveAmmount): ")
                print(path_planning.pathPlanning(speech.lower()))
            elif object_detection.isObjCommand(speech.lower()):
                print("Object to pick up: " + object_detection.object_parse(speech.lower()))
            else:
                print(corpus_and_adapter.response_from_chatbot(speech.)

if __name__ == '__main__':
    #playsound('sounds/cicoremix.mp3')
    main()
