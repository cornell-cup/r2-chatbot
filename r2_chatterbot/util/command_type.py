import face_recognition
import path_planning
import object_detection

def getCommandType(speech):
    if face_recognition.isFaceRecognition(speech):
        response = 'facial recognition'
    elif path_planning.isLocCommand(speech):
        response = 'path planning'
    elif object_detection.isObjCommand(speech):
        response = 'object detection'
    else:
        response = 'not a command'
    return response
