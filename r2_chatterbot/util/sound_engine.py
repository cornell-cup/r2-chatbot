import os
import re
from winsound import PlaySound
from pygame import mixer
import time
from random import randint
from google.cloud import texttospeech

from util.sound_engine_utils import Trie, MORSE_MAP
# try:
#     from .utils import Trie, MORSE_MAP
# except ImportError:
#     from c1c0_sounds.utils import Trie, MORSE_MAP

mixer.init()


class SoundEngine:
    def __init__(self, folder="chirp_parts/", ext=".wav", init_mixer=True, **kwargs):
        self.folder = folder
        if init_mixer:
            mixer.quit()
            mixer.init(**kwargs)
        self.load_chirps(ext=ext)
        self.client = texttospeech.TextToSpeechClient()

    def load_chirps(self, folder=None, ext=".wav", clear_old=True):
        """
        Loads chirps from the path folder.
        PARAMETERS
        ----------
        folder: str
            The path to the folder containing the chirps.
        RETURNS
        -------
        chirps: list
            A list of chirps.
        """
        if clear_old:
            chirp_map = Trie(allow_multiple=True)
        else:
            chirp_map = self.chirp_map
        folder = self.folder if folder is None else folder
        for file in os.listdir(folder):
            if file.endswith(ext):
                chirp_typing = _chirptypes_from_filename(file)
                word, _ = _morse_from_chirptypes(chirp_typing)
                chirp_map[word] = mixer.Sound(os.path.join(folder, file))
        self.chirp_map = chirp_map
        return chirp_map
    
    def audio_from_morse(self, input_):
        """
        Converts a morse code string to a list of chirps.
        PARAMETERS
        ----------
        input_: str
            The morse code string.
        RETURNS
        -------
        chirps: list
            A list of chirps.
        """
        # for c in input_:
        #     if c == ''
        word = input_
        last_word = None
        audio_clips = []
        while len(word)>0 and word != '':
            last_word = word
            audio_clip, _, word = self.chirp_map.traverse(word)
            if word == last_word:
                raise ValueError(f"No chirp found for morse code: {word}")
            # if word == '':
            #     print(f'earlier return clips: {audio_clips} last_word: {last_word}')
            #     return audio_clips
            try:
                # print(f'word: "{word}" audio_clip: {audio_clip}')
                idx = randint(0, len(audio_clip)-1)
                audio_clip = audio_clip[idx]
            except IndexError:
                pass
            audio_clips.append(audio_clip)
        return audio_clips

    def play_audio(self, audio_clips):
        """
        Plays a list of chirps.
        PARAMETERS
        ----------
        audio_clips: list
            A list of chirps.
        """
        # print(audio_clips)
        for audio_clip in audio_clips:
            audio_clip.play()
            while mixer.get_busy():
                pass
    
    def play_morse(self, morse):
        """
        Plays a morse code string.
        PARAMETERS
        ----------
        morse: str
            The morse code string.
        """
        audio_clips = self.audio_from_morse(morse)
        self.play_audio(audio_clips)
    
    def play_text(self, text):
        """
        Plays a text string.
        PARAMETERS
        ----------
        text: str
            The text string.
        """
        morse = _morse_from_text(text)
        morses = morse.split(' ')
        for morse_ in morses:
            self.play_morse(morse_)
            time.sleep(0.3)

    def text_to_speech(self, input_text):

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=input_text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open("output.mp3", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')
        PlaySound("output.mp3")


def _chirptypes_from_filename(chirp_name):
    """
    Interprets the chirp name to determine the chirp type.
    PARAMETERS
    ----------
    chirp_name: str
        The name of the chirp.
    RETURNS
    -------
    chirp_type: str
        The chirp types.
    """
    chirp_types = list(re.findall(r'(\d+[LS])(?:_\d+[LS])*(\d+)', chirp_name)[0])
    for match in re.findall(r'_\d[LS]*', chirp_name):
        chirp_types.insert(len(chirp_types) - 1, match[1:])
    return tuple(chirp_types)

def _morse_from_chirptypes(chirp_types):
    """
    Creates a filename from the chirp types.
    PARAMETERS
    ----------
    chirp_types: tuple
        The chirp types.
    RETURNS
    -------
    filename: str
        The filename.
    """
    chirps, count = chirp_types[:-1], chirp_types[-1]
    word = ''
    for chirp in chirps:
        char_count = int(chirp[:-1])
        char_ = chirp[-1]
        if char_ not in ('L', 'S'):
            raise ValueError(f"Invalid chirp type: {chirp}")
        word += '.'*char_count if char_ == 'S' else '-'*char_count
    return word, count

def _morse_from_text(text):
    """
    Creates a morse code string from the text string.
    PARAMETERS
    ----------
    text: str
        The text string.
    RETURNS
    -------
    morse: str
        The morse code string.
    """
    text = text.lower()
    morse = ''
    for char in text:
        if char not in MORSE_MAP:
            raise ValueError(f"Invalid character: {char}")
        morse += MORSE_MAP[char]
    return morse
