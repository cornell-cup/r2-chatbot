from util import live_streaming
from util import nlp_util
from util import keywords
from util import make_response
from util import playtrack
from util import path_planning
from util import object_detection
from util import face_recognition
from util import utils
#from util.api import weather
#from util.api import restaurant
from playsound import playsound
import re
import sys
import os
import corpus_and_adapter
import re

# for flask setup
import requests
import json
import io
import socket

from multiprocessing import Process
import subprocess
import os

# import C1C0-specific subsystems as available
import locomotion_cmd
# facial recognition

print(os.getcwd())
credential_path = "api_keys/speech_to_text.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

url = "http://18.216.143.187/"

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
                if os.getppid() > 50: # only run if this process is a child process (see description below)
                    face_cmd = face_recognition.faceRecog(speech)
                    print(face_cmd) 
                # task is to transfer over to facial recognition client program
                # TODO: once facial recognition package is ready and the chatbot command
                # is compatible, uncomment/correct the following line:
                # p = Process(target=c1c0_facialrecognition.run, args=(face_cmd,)
                # p.start()
            elif path_planning.isLocCommand(speech.lower()):
                if os.getppid() < 50: # this check uses process IDs so that this only runs
                                    # if it was spawned from a different python process
                                    # as a child, since those processes spawned from the 
                                    # linux command line typically have values less than 10
                                    # while those spawned as a child process have typical values
                                    # in the hundreds
                    cmd = path_planning.pathPlanning(speech.lower())
                    # locomotion_cmd.chatbot_move(cmd)                     
                    print("Move command (itemMove, direction, moveAmmount): ")
                    print(path_planning.pathPlanning(speech.lower()))
                    return cmd # don't worry, this only returns/exits the loop in the process handling locomotion
                               # chatbot main will get re-scheduled as soon as locomotion is handled
                # task is to transfer over to path planning on the system
            elif object_detection.isObjCommand(speech.lower()):
                #print("Object to pick up: " + object_detection.object_parse(speech.lower()))
                # run object detection `onjetson` - gets image of object facing C1C0's camera
                # this will run the object detection program in parallel as a separate process
                if os.getppid() > 50: # only run if this process is a child (see description above)
                    subprocess.Popen(['python3','objectdetection.py'])                
            else:
                # we don't want the text to be lowercase since it messes with location detection
                print(corpus_and_adapter.response_from_chatbot(speech))
                # send this element to AWS for response generation

                #begin the flask transfer now

if __name__ == '__main__':
    #playsound('sounds/cicoremix.mp3')
    main()
