from google.cloud.speech_v1p1beta1.types.resource import CustomClass

def movement_class():
  movement_words = ["move", "go", "turn", "rotate"]
  name = "Movement Words"
  custom_class_id = "movement_words"
  class_items = list(map(lambda word: CustomClass.ClassItem(value=word), movement_words ))
  movement_class = CustomClass(name=name, custom_class_id=custom_class_id, items=class_items)
  return movement_class

def direction_class():
  #phrase
  # s and words included
  direction_words = ["forward","forwards","backward","backwards","back","left","right","clockwise","counterclockwise","to the left","to the right"]
  name = "Direction Words"
  custom_class_id = "direction_words"
  class_items = list(map(lambda word: CustomClass.ClassItem(value=word),direction_words ))
  direction_class = CustomClass(name=name, custom_class_id=custom_class_id,items=class_items)
  return direction_class 

def unit_class():
  unit_words = ["meter","meters","feet","foot","degrees","radians"]
  name = "Unit Words"
  custom_class_id = "unit_words"
  class_items = list(map(lambda word: CustomClass.ClassItem(value=word),unit_words ))
  unit_class = CustomClass(name=name, custom_class_id=custom_class_id,items=class_items)
  return unit_class

movement_custom_class = movement_class()
if __name__ == '__main__':
  # print(list(inspect.getmembers(google_speech, inspect.isclass)))
  movement_class()
  direction_class()
  unit_class()

