CHATBOT_PATH := $(shell pwd)
PYTHON_VER   := 3.11

run:
	venv/bin/python chatbot.py

install:
	venv/bin/pip install -r requirements.txt

venv:
	python$(PYTHON_VER) -m venv venv/
	venv/bin/pip install --upgrade pip setuptools wheel
