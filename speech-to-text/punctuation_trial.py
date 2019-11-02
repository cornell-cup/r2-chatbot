from google.cloud import speech_v1p1beta1
import io


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file with punctuation

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1p1beta1.SpeechClient()

     local_file_path = 'resources/weatherQuestion.wav'

    # When enabled, trascription results may include punctuation
    # (available for select languages).
    enable_automatic_punctuation = True

    # The language of the supplied audio. Even though additional languages are
    # provided by alternative_language_codes, a primary language is still required.
    language_code = "en-US"
    config = {
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "language_code": language_code,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
