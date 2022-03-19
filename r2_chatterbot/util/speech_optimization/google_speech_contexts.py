from google.cloud.speech_v1p1beta1.types.resource import CustomClass

def create_custom_class(words, name, custom_class_id):
  class_items = list(map(lambda word: CustomClass.ClassItem(value=word), words))
  return CustomClass(name=name, custom_class_id=custom_class_id, items=class_items)

lin_movement_class = create_custom_class(words = ["move", "go"],
  name = "Linear Move Verbs", custom_class_id = "l_move")

rot_movement_class = create_custom_class(words = ["turn", "rotate"],
  name = "Rotational Move Verbs", custom_class_id = "r_move")

lin_dir_class = create_custom_class(
  words = ["forward","backward", "back","left","right","to the right", "to the left"],
  name = "Linear Directions", custom_class_id="l_dir")

rot_dir_class = create_custom_class(
  words = ["right", "left", "to the right", "to the left", "clockwise", "counterclockwise"],
  name = "Rotational Directions", custom_class_id="r_dir")

lin_unit_class = create_custom_class(words = ["meter","meters","feet","foot"], 
  name="Linear Units", custom_class_id="l_unit")

rot_unit_class = create_custom_class(words = ["degrees", "radians"], 
  name="Rotational Units", custom_class_id="r_unit")

# def create_unit_class():
#   unit_words = ["meter","meters","feet","foot","degrees","radians"]
#   name = "Unit Words"
#   custom_class_id = "units"
#   class_items = list(map(lambda word: CustomClass.ClassItem(value=word),unit_words ))
#   unit_class = CustomClass(name=name, custom_class_id=custom_class_id,items=class_items)
#   return unit_class

# direction_custom_class = create_direction_class()
# unit_custom_class = create_unit_class()

