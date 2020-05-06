# c1c0-chatbot
### Stanley Lin, Haomiao Liu, Charu Murugesan, Rishi Malhotra, Sahar Sami, Jerry Guo, Matt Bean

This repository contains code for the chatbot project for Cornell Cup Robotics which was developed Fall 2019 - Spring 2020.

## Installation

Make sure you have Python 3 and at least Java 8. Also make sure you have `pip`.

The following modules are needed: `nltk rake-nltk playsound pyaudio google-cloud-speech geocoder chatterbot chatterbot-corpus`

If you encounter difficulties, try checking the Installation Issues section.

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

## Running test scripts
Inside the `test` directory, there are several scripts used for testing components of the system. If you are unable to run them within the test directory due to import errors, you can move them into the root of the project and run them from there.

## Project Structure
* `api_keys`: all api key files go here (txt, json, etc.). DO NOT PUSH THE KEYS TO THIS REPO. All the necessary keys are on Google Drive
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
You can either acquire your own version of these, or download the ones in the Cornell Cup drive (under (under "Cornell Cup 19-20/C1C0/Chatbot/api keys")

The following files are necessary under the `api_keys/` directory:
* `geonames_username.txt`: a user name on the [geonames](http://www.geonames.org/) site
* `open_weather.txt`: an api key from [OpenWeatherMap](https://openweathermap.org/api)
* `restaurant_api.txt`: an api key from [Zomato](https://developers.zomato.com/api)
* `speech_to_text.json`: a Google Cloud Platform [service account](https://cloud.google.com/compute/docs/access/service-accounts) private key

## Installation Issues

### `pyaudio` Not Installing
You may be missing a library called portaudio. Instead of installing through `pip`, you can try to installing through your system's package manager.

On your system's package manager, first try searching for pyaudio. If it exists, there's a good chance that it will also install portaudio for you, so install it. If not, search for a package containing the word "portaudio". If there is, install it.

### `playaudio` Not Running on Mac
* First run `pip uninstall AppKit`
* Now install `gobject-introspection libffi` using the system package manager (ex: Homebrew)
* Also set the environment variable `PKG_CONFIG_PATH=/usr/local/Cellar/libffi/<version number>/lib/pkgconfig/`
* Run `pip install --upgrade --force-reinstall PyObjC PyObjC-core`

