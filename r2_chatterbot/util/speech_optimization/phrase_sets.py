from google.cloud.speech_v1p1beta1.types import PhraseSet

def movement_phrases():
  """
  examples:
  
  """
  name = "movement_phrases"
  phrases = [
    "${movement_words} $OPERAND"
    "${units} ${directions}",
    "${movement_words} ${units}",
    "$OPERAND ${directions}",
    "${movement_words}", 
    "${directions}"
  ]
  boost_value = 20
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases))
  movement_phrase_set = PhraseSet(name=name, phrases=class_items, boost=boost_value)
  return movement_phrase_set


def number_first_phrase():
  name = "number_first_phrase"
  return PhraseSet(name=name, phrases=[PhraseSet.Phrase(value="${movement_words} $OPERAND ${units} ${directions}")], boost=10)

def direction_first_phrase():
  name = "direction_first_phrase"
  return PhraseSet(name=name, phrases=[PhraseSet.Phrase(value="${movement_words} ${units} $OPERAND ${directions}")], boost=10)

def common_phrases():
  name = "common_phrases"
  phrases = ["Cornell Cup Robotics","Hey cico","Pick up","grab","Cornell", "cico", "kiko"]
  boost_value = 30  #this may change 
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word), phrases ))
  common_phrase_set = PhraseSet(name=name, phrases= class_items, boost = boost_value)
  return common_phrase_set

 
movement_phrase_set = movement_phrases()
number_first_phrase_set = number_first_phrase()
direction_first_phrase_set = direction_first_phrase()
common_phrase_set = common_phrases()
