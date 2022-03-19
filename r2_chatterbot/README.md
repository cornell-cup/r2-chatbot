# c1c0-chatbot

This repository contains code for the chatbot project for Cornell Cup Robotics which was developed Fall 2019 - Spring 2022.

### Spring 2022 Team:
Sahar Sami, Jerry Guo, Junyu Wang, Bahaa Kotb, Vincent Jiang

### Fall 2021 Team:
Sahar Sami, Jerry Guo, Junyu Wang, Anthony Cuturrufo, Bahaa Kotb, Anant Shyam

### Spring 2021 Team:
Sahar Sami, Jerry Guo, Junyu Wang, Anthony Cuturrufo

### Spring 2021 Team:
Sahar Sami, Jerry Guo, Dhruv Sreenivas, Yuyi He, Junyu Wang, Anthony Cuturrufo

### Fall 2020 Team:
Sahar Sami, Jerry Guo, Matt Bean, Dhruv Sreenivas, Yuyi He

### Spring 2020 Team:
Stanley Lin, Charu Murugesan, Sahar Sami, Jerry Guo, Matt Bean

### Fall 2019 Team:
Stanley Lin, Haomiao Liu, Charu Murugesan, Rishi Malhotra



## Installation

0. Make sure you have Python 3 and at least Java 8. Also make sure you have `pip`. (Recommended: Use Anaconda as your Python distribution and create a virtual environment with Python 3.8+ for all Chatbot work)

1. Install PyAudio using the following instructions depending on your operating system and distribution:
    1. Windows: `conda install pyaudio` or `pip install pyaudio`
    2. Mac OS X: `brew install portaudio`, then `pip install pyaudio` 
    3. Ubuntu: first install the portaudio19-dev package, then run `sudo apt-get install python-pyaudio python3-pyaudio`
	
2. Run 'pip install -r requirements.txt" to install all other requirements."

### Setting Up Named Entity Recognition
You will need to download the Stanford Named Entity Recognizer (NER) from [here](https://nlp.stanford.edu/software/CRF-NER.shtml). Unzip the resulting file and rename the folder to `stanford-ner` and move it into the `dep/` directory. The `dep/` directory should look like
```
dep/
	stanford-ner/
		...
	...
```

##### Additional instructions for Windows
It may be necessary to set the `JAVAHOME` environment variable. Make sure to point this at where your JDK is located.

## Running the project
Run `python main.py`

You may get prompts from NLTK to install additional packages/dependencies. If this is the case, you can just start a python interpreter on your terminal and run the commands that it specifies. 

All interactions with the chatbot require you to begin by saying "Hey C1C0," followed by the query. This was intended to avoid false positive interactions.

### Instructions for running the locomotion, facial recognition, and object detection
* For running locomotion commnads, the command must contain the object to move, distance to move it, and direction to move it. Otherwise it will not be detected as a locomotion command. This function will return a triple with that information.
* For running the facial recognition command, the command must contain one of the following words: `{"wave", "hello", "hi", "check", "attendance", "call me", "greetings", "what's up" }`. Then it will determine what type of facial recognition command this is.
* For running the object detection command, the command must include the object to pick up. The object can be multiple words, such as "water bottle" or "graphing calculator." 

## Running test scripts
Inside the `test` directory, there are several scripts used for testing components of the system. If you are unable to run them within the test directory due to import errors, you can move them into the root of the project and run them from there.

## Project Structure
* `api_keys`: all api key files go here (txt, json, etc.). **DO NOT PUSH THE KEYS TO THIS REPO**. All the necessary keys are on Google Drive (check the API keys section for more info)
* `data`: contains miscellaneous data needed in the execution of the program
* `dep`: contains external dependencies
* `logic_adapters`: contains logic adapters for use with Chatterbot
* `misc`: miscellaneous files
* `sounds`: contains sound files to be outputted through the speaker
* `tests`: contains scripts to test components of the system
* `util`: where all the modules in the project go. See the Modules section for more information
* `main.py`: the entrypoint of the program

## Modules
Our project contains the following modules, all contained within the `util` directory:
* `face_recognition`: parses text commands related to facial recognition
* `keywords`: get keywords from a phrase, also implements code to utilize functions in `topic_tests`
* `live_streaming`: code for speech to text system
* `make_response`: generates a phrase based on various pieces of data
* `nlp_util`: convenience functions to accomplish various Natural Language Processing (NLP) tasks
* `object_detection`: parses text commands related to object detection
* `path_planning`: parses text commands related to locomotion/path planning
* `playtrack`: contains code to play audio files
* `topic_tests`: all functions in this module test for a specific topic in a phrase. Should be used with `keywords.get_topic()`.
* `utils`: contains miscellaneous funtionality

Within `util/api`, we also have modules to handle API interactions:
* `weather`: interfaces with the OpenWeatherMap API
* `restaurant`: interfaces with the Zomato API

## API keys
Some of these keys can be downloaded from the Cornell Cup drive (under "Cornell Cup 20-21/C1C0/C1C0 CS/Chatbot/api keys").

It is *highly* advised that you find your own versions of these keys, as the ones in the drive may no longer be valid

**DO NOT PUSH KEYS TO THIS REPO**.

The following files are necessary under the `api_keys/` directory:
* `geonames_username.txt`: a user name on the [geonames](http://www.geonames.org/) site
* `open_weather.txt`: an api key from [OpenWeatherMap](https://openweathermap.org/api)
* `restaurant_api.txt`: an api key from [Zomato](https://developers.zomato.com/api)
* `speech_to_text.json`: a Google Cloud Platform [service account](https://cloud.google.com/compute/docs/access/service-accounts) private key

## Installation Issues

### `pyaudio` Not Installing
You may be missing a library called portaudio. Instead of installing through `pip`, you can try to installing through your system's package manager.

On your system's package manager, first try searching for `pyaudio`. If it exists, there's a good chance that it will also install portaudio for you, so install it. If not, search for a package containing the word "portaudio". If there is, install it.

### `playaudio` Not Running on Mac
* First run `pip uninstall AppKit`
* Now install `gobject-introspection libffi` using the system package manager (ex: Homebrew)
* Also set the environment variable `PKG_CONFIG_PATH=/usr/local/Cellar/libffi/<version number>/lib/pkgconfig/`
* Run `pip install --upgrade --force-reinstall PyObjC PyObjC-core`

### `AttributeError: module 'chatterbot.comparisons' has no attribute 'levenshtein_distance'`
See [this](https://github.com/gunthercox/ChatterBot/issues/1712) link

### `OSError: Can't find model 'en'`
Run `python -m spacy download en_core_web_sm`. If you tried that and it still doesn't work, that may mean that the model was installed for the wrong python version. In that case, try:
* not running the program with `sudo`
* deactivating your virtual environment, if you are using one
* this [thread](https://stackoverflow.com/questions/49964028/spacy-oserror-cant-find-model-en)

