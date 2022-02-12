from google.cloud.speech_v1p1beta1.types.resource import CustomClass

def movement_class():
  movement_words = ["move", "go", "turn", "rotate"]
  name = "Movement Words"
  custom_class_id = "movement_words"
  class_items = list(map(lambda word: CustomClass.ClassItem(value=word), movement_words ))
  movement_class = CustomClass(name=name, custom_class_id=custom_class_id, items=class_items)
  return movement_class


movement_custom_class = movement_class()