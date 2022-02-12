import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import google.cloud.speech_v1p1beta1.types as google_speech
# from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1.types.resource import CustomClass
import inspect

def movement_class():
  movement_words = ["move", "go", "turn", "rotate"]
  name = "Movement Words"
  custom_class_id = "movement_words"
  class_items = list(map(lambda word: CustomClass.ClassItem(value=word), movement_words ))
  movement_class = CustomClass(name=name, custom_class_id=custom_class_id, items=class_items)
  return movement_class


movement_custom_class = movement_class()

if __name__ == '__main__':
  # print(list(inspect.getmembers(google_speech, inspect.isclass)))
  movement_class()