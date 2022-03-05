from google.cloud.speech_v1p1beta1.types import PhraseSet

def movement_phrases():
  """
  examples:
  
  """
  name = "movement_phrases"
  phrases = [
    "${movement_words} $OPERAND",
    "${units} ${directions}",
    "${movement_words} ${units}",
    "$OPERAND ${directions}",
    "$OPERAND ${units}",
    "${units} $OPERAND",
    "${movement_words}",
    "${directions}"    
  ]
  boost_value = 13
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases))
  movement_phrase_set = PhraseSet(name=name, phrases=class_items, boost=boost_value)
  return movement_phrase_set


def cico_phrases():
  name = "cico_phrases"
  phrases = ["Hey cico","cico", "kiko"]
  boost_value = 20  #this may change 
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases ))
  phrase_set = PhraseSet(name=name, phrases= class_items, boost = boost_value)
  return phrase_set

def common_phrases():
  name = "common_phrases"
  phrases = ["Cornell Cup Robotics", "pick up", "grab","Cornell"]
  boost_value = 15  #this may change 
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases ))
  common_phrase_set = PhraseSet(name=name, phrases= class_items, boost = boost_value)
  return common_phrase_set

def grab_phrases():
  name = "grab_phrases"
  phrases = ["grab","pick up"]
  boost_value = 8 #this may change 
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases))
  grab_phrase_set = PhraseSet(name = name, phrases = class_items, boost = boost_value)
  return grab_phrase_set

 
movement_phrase_set = movement_phrases()
cico_phrase_set = cico_phrases()
common_phrase_set = common_phrases()
grab_phrase_set = grab_phrases()
