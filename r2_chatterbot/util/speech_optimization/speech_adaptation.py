import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from util.speech_optimization.google_speech_contexts import movement_custom_class
from util.speech_optimization.phrase_sets import movement_phrase_set
from google.cloud.speech_v1p1beta1.types import SpeechAdaptation

speech_adaptation_object = SpeechAdaptation(
  phrase_sets = [movement_phrase_set],
  phrase_set_references = [],
  custom_classes = [movement_custom_class]
)