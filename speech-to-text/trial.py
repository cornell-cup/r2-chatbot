import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def convert_to_text(audio_file_name,sampling_rate):
    """
    Returns a tuple (string output,confidence)
    Converts speech into
     and RETURNS a string output

    Parameter: audio_file_name - the name of the audio file_name
    Precondition: must be of the wav format

    Parameter: sampling_rate is the rate at which audio is sampled
    Precondition: must be an int
    """
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        audio_file_name)

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sampling_rate,
        language_code='en-US',audio_channel_count=2)

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    #DO NOT UNCOMMENT
    # for result in response.results:
    #     print('Transcript: {}'.format(result.alternatives[0].transcript))

    output_string = '{}'.format(response.results[0].alternatives[0].transcript)
    output_confidence = '{}'.format(response.results[0].alternatives[0].confidence)
    return (output_string,output_confidence)

def get_string(t):
    """
    Returns the output string (1st element of the tuple)

    Parameter: t is a tuple
    Precondition: the first element is a string, second is a float
    """
    return t[0]

def get_confidence(t):
    """
    Returns the confidence (2nd element of the tuple)

    Parameter: t is a tuple
    Precondition: the first element is a string, second is a float
    """
    return t[1]
