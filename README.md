# c1c0-chatbot
### Stanley Lin, Haomiao Liu, Charu Murugesan, Rishi Malhotra

This repository contains code for the chatbot project for Cornell Cup Robotics which was developed Fall 2019 - Spring 2020.

## Installation

Make sure you have python 3. Also make sure you have `pip`.

The following modules are needed: `nltk rake-nltk playsound pyaudio google-cloud-speech geocoder`

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

## Installation Issues

### `pyaudio` Not Installing
You may be missing a library called portaudio. Instead of installing through `pip`, you can try to installing through your system's package manager.

On your system's package manager, first try searching for pyaudio. If it exists, there's a good chance that it will also install portaudio for you, so install it. If not, search for a package containing the word "portaudio". If there is, install it.

### `playaudio` Not Running on Mac
* First run `pip uninstall AppKit`
* Now install `gobject-introspection libffi` using the system package manager (ex: Homebrew)
* Also set the environment variable `PKG_CONFIG_PATH=/usr/local/Cellar/libffi/<version number>/lib/pkgconfig/`
* Run `pip install --upgrade --force-reinstall PyObjC PyObjC-core`

