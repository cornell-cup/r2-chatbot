# c1c0-chatbot
### Stanley Lin, Haomiao Liu, Charu Murugesan, Rishi Malhotra, Sahar Sami, Jerry Guo, Matt Bean

This repository contains code for the chatbot project for Cornell Cup Robotics which was developed Fall 2019 - Spring 2020.

## Installation

Make sure you have Python 3 and at least Java 8. Also make sure you have `pip`.

The following modules are needed: `nltk rake-nltk playsound pyaudio google-cloud-speech geocoder chatterbot chatterbot-corpus`

Additionally, you will need to download the Stanford Named Entity Recognizer (NER) from [here](https://nlp.stanford.edu/software/CRF-NER.shtml). Unzip the resulting file and rename the folder to `stanford-ner` and move it into the `dep/` directory. The `dep/` directory should look like
```
dep/
	stanford-ner/
		...
```

##### Additional instructions for Windows
It may be necessary to set the `JAVAHOME` environment variable. Make sure to point this at where your JDK is located

If you encounter difficulties, try checking the Installation Issues section.

### Setting Up Boost for Speech to Text
Navigate to the directory where your `pip` packages are installed.

You can find where packages are installed with
```python
import site

# in one of these two locations
site.getsitepackages()
site.getusersitepackages()
```

Now, do the following:
* Go to the `google/cloud` directory.
* Copy the file `speech_v1p1beta1/proto/cloud_speech_pb2.py` to `speech_v1/proto/` and overwrite the file

## Running the project
Run `python main.py`

## Project Structure
* `api_keys`: all api key files go here (txt, json, etc.). DO NOT PUSH THE KEYS TO THIS REPO. All the necessary keys are on Google Drive
* `data`: contains miscellaneous data needed in the execution of the program
* `misc`: miscellaneous files
* `sounds`: contains sound files to be outputted through the speaker
* `tests`: contains scripts to test components of the system
* `util`: where all the modules in the project go. See the Modules section for more information
* `main.py`: the entrypoint of the program

## Modules
Our project contains the following modules, all contained within the `util` directory:
* `keywords`: get keywords from a phrase, also implements code to utilize functions in `topic_tests`
* `live_streaming`: code for speech to text system
* `make_response`: generates a phrase based on various pieces of data
* `nlp_util`: convenience functions to accomplish various Natural Language Processing (NLP) tasks
* `playtrack`: contains code to play audio files
* `topic_tests`: all functions in this module test for a specific topic in a phrase. Should be used with `keywords.get_topic()`.
* `utils`: contains miscellaneous funtionality

Within `util/api`, we also have modules to handle API interactions:
* `weather`: interfaces with the OpenWeatherMap API
* `restaurant`: interfaces with the Zomato API

## API keys
The following files are necessary under the `api_keys/` directory:
* `geonames_username.txt`: a user name on the [geonames](http://www.geonames.org/) site
* `open_weather.txt`: an api key from [OpenWeatherMap](https://openweathermap.org/api)
* `restaurant_api.txt`: an api key from [Zomato](https://developers.zomato.com/api)
* `Speech to Text-bef030531cd1.json`: a Google Cloud Platform [service account](https://cloud.google.com/compute/docs/access/service-accounts) private key

## Installation Issues

### `pyaudio` Not Installing
You may be missing a library called portaudio. Instead of installing through `pip`, you can try to installing through your system's package manager.

On your system's package manager, first try searching for pyaudio. If it exists, there's a good chance that it will also install portaudio for you, so install it. If not, search for a package containing the word "portaudio". If there is, install it.

### `playaudio` Not Running on Mac
* First run `pip uninstall AppKit`
* Now install `gobject-introspection libffi` using the system package manager (ex: Homebrew)
* Also set the environment variable `PKG_CONFIG_PATH=/usr/local/Cellar/libffi/<version number>/lib/pkgconfig/`
* Run `pip install --upgrade --force-reinstall PyObjC PyObjC-core`

