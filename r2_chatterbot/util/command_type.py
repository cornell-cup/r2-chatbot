import face_recognition_utils
import path_planning
import object_detection


def getCommandType(speech, question, question_type):
    if face_recognition_utils.isFaceRecognition(speech)[0]:
        response = 'facial recognition'
    elif (not question or question_type
          == 'yes/no question') and path_planning.isLocCommand(speech):
        response = 'path planning'
    elif (not question or question_type
          == 'yes/no question') and object_detection.isObjCommand(speech):
        response = 'object detection'
    else:
        response = 'not a command'
    return response
