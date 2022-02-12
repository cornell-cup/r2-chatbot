import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from speech_adaptation.google_speech_contexts import movement_custom_class
from speech_adaptation.phrase_sets import movement_phrase_set