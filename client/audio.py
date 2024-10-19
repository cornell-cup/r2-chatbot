from client.config import FUZZY_THRESHOLD

import numpy as np
import sounddevice as sd
import speech_recognition as sr

from fuzzywuzzy import fuzz

# Source: https://stackoverflow.com/questions/55984129/attributeerror-could-not-find-pyaudio-check-installation-cant-use-speech-re
class DuckTypedMicrophone( sr.AudioSource ):
    def __init__(self, device=None, samplerate=44100, channels=1):
        self.device     = device
        self.samplerate = samplerate
        self.channels   = channels

    def __enter__(self):
        self._stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, device=self.device)
        self._stream.start()

        self.CHUNK        = 1024
        self.SAMPLE_RATE  = self.samplerate
        self.SAMPLE_WIDTH = 2  # Assuming 16-bit samples
        return self

    def __exit__(self, *args):
        self._stream.stop()
        self._stream.close()

    def read(self, n_samples):
        audio_data = self._stream.read(n_samples)
        return np.int16(audio_data[0] * 32767).tobytes()  # Convert to 16-bit PCM

    @property
    def stream(self):
        return self


def speech_to_text():
    recognizer = sr.Recognizer()

    with DuckTypedMicrophone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("\033[94mWaiting for audio...\033[0m")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError or sr.RequestError:
            return None


def recognize_C1C0(message: str) -> bool:
    names = ["Hey C1C0", "Hey Kiko", "Hey Keko", "Hey Kee Koh", "Hey Chico", "Hey Chica"]
    _, score = fuzzy_match(message, names)
    print("Fuzz: ", score)
    return score >= FUZZY_THRESHOLD


def fuzzy_match(text, targets):
    scores = [fuzz.partial_ratio(text, target) for target in targets]
    return targets[np.argmax(scores)], np.max(scores)
