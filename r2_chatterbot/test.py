
from google.cloud import speech_v1p1beta1 as speech


def transcribe_with_model_adaptation(
    project_id, location, storage_uri, custom_class_id, phrase_set_id
):

    """
    Create`PhraseSet` and `CustomClasses` to create custom lists of similar
    items that are likely to occur in your input data.
    """

    # Create the adaptation client
    adaptation_client = speech.AdaptationClient()

    # The parent resource where the custom class and phrase set will be created.
    parent = f"projects/{project_id}/locations/{location}"

    # Create the custom class resource
    adaptation_client.create_custom_class(
        {
            "parent": parent,
            "custom_class_id": custom_class_id,
            "custom_class": {
                "items": [
                    {"value": "sushido"},
                    {"value": "altura"},
                    {"value": "taneda"},
                ]
            },
        }
    )
    custom_class_name = (
        f"projects/{project_id}/locations/{location}/customClasses/{custom_class_id}"
    )
    # Create the phrase set resource
    phrase_set_response = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": phrase_set_id,
            "phrase_set": {
                "boost": 10,
                "phrases": [
                    {"value": f"Visit restaurants like ${{{custom_class_name}}}"}
                ],
            },
        }
    )
    phrase_set_name = phrase_set_response.name
    # The next section shows how to use the newly created custom
    # class and phrase set to send a transcription request with speech adaptation

    # Speech adaptation configuration
    speech_adaptation = speech.SpeechAdaptation(phrase_set_references=[phrase_set_name])

    # speech configuration object
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,
        language_code="en-US",
        adaptation=speech_adaptation,
    )

    # Create the speech client
    speech_client = speech.SpeechClient()

    response = speech_client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

transcribe_with_model_adaptation("speechtest", "speechtest", "")