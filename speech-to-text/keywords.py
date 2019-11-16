from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums


def sample_recognize(storage_uri, phrase):
    """
    Transcribe a short audio file with speech adaptation.

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
      phrase Phrase "hints" help recognize the specified phrases from your audio.
    """

    client = speech_v1p1beta1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.mp3'
    # phrase = 'Brooklyn Bridge'
    phrases = [phrase]

    # Hint Boost. This value increases the probability that a specific
    # phrase will be recognized over other similar sounding phrases.
    # The higher the boost, the higher the chance of false positive
    # recognition as well. Can accept wide range of positive values.
    # Most use cases are best served with values between 0 and 20.
    # Using a binary search happroach may help you find the optimal value.
    boost = 20.0
    speech_contexts_element = {"phrases": phrases, "boost": boost}
    speech_contexts = [speech_contexts_element]

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "speech_contexts": speech_contexts,
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
