import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from util.speech_optimization.google_speech_contexts import *
from util.speech_optimization.phrase_sets import common_phrase_set, movement_phrase_set, cico_phrase_set
from google.cloud.speech_v1p1beta1.types import SpeechAdaptation

speech_adaptation_object = SpeechAdaptation(
  phrase_sets = [movement_phrase_set, common_phrase_set, cico_phrase_set],
  phrase_set_references = [],
  custom_classes = [lin_movement_class, rot_movement_class, lin_dir_class, rot_dir_class, 
    lin_unit_class, rot_unit_class]
)