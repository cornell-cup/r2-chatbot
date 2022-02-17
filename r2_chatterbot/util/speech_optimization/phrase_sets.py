from google.cloud.speech_v1p1beta1.types import PhraseSet

def movement_phrases():
  """
  examples:
  
  """
  name = "Movement Phrases"
  phrases = [
    "${movement-words} $OPERAND ${unit} ${direction-word}",
    "${movement-words} ${unit}  ${OPERAND} ${direction-word}",
    "${movement_words}",
    "${direction-word}"
  ]
  boost_value = 10 # this may change
  class_items = list(map(lambda word: PhraseSet.Phrase(value=word, boost=boost_value), phrases))
  movement_phrase_set = PhraseSet(name=name, phrases=class_items, boost=boost_value)
  return movement_phrase_set

def common_phrases():
  pass


movement_phrase_set = movement_phrases()