from google.cloud.speech_v1p1beta1.types import PhraseSet


def movement_phrases():
  """
  examples:
  
  """
  name = "movement_phrases"
  phrases = [
    "${l_move} $OPERAND",
    "${r_move} $OPERAND",
    "${l_unit} ${l_dir}",
    "${r_unit} ${r_dir}",
    "${l_move} ${l_unit}",
    "${r_move} ${r_unit}",
    "$OPERAND ${l_dir}",
    "$OPERAND ${r_dir}",
    "$OPERAND ${l_unit}",
    "$OPERAND ${r_unit}",
    "${l_unit} $OPERAND",
    "${r_unit} $OPERAND",
    "${l_dir}",
    "${r_dir}"    
  ]
  boost_value = 13
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases))
  movement_phrase_set = PhraseSet(name=name, phrases=class_items, boost=boost_value)
  return movement_phrase_set


def cico_phrases():
  name = "cico_phrases"
  phrases = ["cico", "kiko","Hey","Hey Kiko","Hey cico"]
  boost_value = 20  #this may change 
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases ))
  phrase_set = PhraseSet(name=name, phrases= class_items, boost = boost_value)
  return phrase_set


def object_detection_phrases():
  name = "od_phrases"
  phrases = ["pick up", "grab", "get", "take"]
  boost_value = 8
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases ))
  phrase_set = PhraseSet(name=name, phrases= class_items, boost = boost_value)
  return phrase_set


def common_phrases():
  name = "common_phrases"
  phrases = ["Cornell Cup Robotics", "Cornell"]
  boost_value = 12  #this may change 
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases ))
  common_phrase_set = PhraseSet(name=name, phrases= class_items, boost = boost_value)
  return common_phrase_set

 
movement_phrase_set = movement_phrases()
cico_phrase_set = cico_phrases()
common_phrase_set = common_phrases()
object_grab_phrase_set = object_detection_phrases()
