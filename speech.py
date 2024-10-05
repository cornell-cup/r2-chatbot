import audiomath; audiomath.RequireAudiomathVersion( '1.12.0' )
import speech_recognition as sr

# Source: https://stackoverflow.com/questions/55984129/attributeerror-could-not-find-pyaudio-check-installation-cant-use-speech-re
class DuckTypedMicrophone( sr.AudioSource ):
    def __init__(self, device=None, chunkSeconds=512/44100.0):
        self.recorder     = None
        self.device       = device
        self.chunkSeconds = chunkSeconds

    def __enter__( self ):
        self.nSamplesRead = 0
        self.recorder     = audiomath.Recorder(audiomath.Sound(5, nChannels=1), loop=True, device=self.device)

        # Attributes required by Recognizer.listen():
        self.CHUNK        = audiomath.SecondsToSamples(self.chunkSeconds, self.recorder.fs, int)
        self.SAMPLE_RATE  = int(self.recorder.fs)
        self.SAMPLE_WIDTH = self.recorder.sound.nbytes
        return self

    def __exit__(self, *blx):
        self.recorder.Stop()
        self.recorder = None

    def read(self, nSamples):
        sampleArray        = self.recorder.ReadSamples(self.nSamplesRead, nSamples)
        self.nSamplesRead += nSamples
        return self.recorder.sound.dat2str(sampleArray)

    @property
    def stream(self):
        return self if self.recorder else None


def speech_to_text():
    recognizer = sr.Recognizer()

    with DuckTypedMicrophone() as source:
        print("Please wait. Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            print("Please speak something...")
            audio = recognizer.listen(source, phrase_time_limit=5)
            print("Recognizing...")

            try:
                text = recognizer.recognize_google(audio)
                print("You said: " + text)
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError:
                print("Sorry, I could not request results from Google.")

# Call the function to test
speech_to_text()
