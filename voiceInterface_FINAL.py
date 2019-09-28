"""
File Created by Yanchen Zhan '22 (yz366)
     Help from  Christian Polydor '21 (cp456)
				Varun Maheshwari '22 (vm324)
				Viren Shah '21 (vvs24)
				R2 CS Subteam
"""

"""
spoken_text = listen(r, mic)
spoken_text = spoken_text.lower()
"""

#spoken = input("enter command or sentence: ")

### import respective packages ###

#for voice recognition
import math
from gcc_phat import gcc_phat
import numpy as np
import json
import simpleaudio as sa
import sys
import speech_recognition as sr
import pyaudio

#api key for Cortical - keyword parser
#use retina_sdk_florida.txt for florida
import retinasdk
liteClient = None
with f as open("api_keys/retina_sdk.txt"):
    key = f.read().strip()
    liteClient = retinasdk.LiteClient(key)

#for Watson sentiment analysis
import retinasdk
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
from watson_developer_cloud import NaturalLanguageUnderstandingV1

naturalLanguageUnderstanding = None
with f as open("api_keys/watson.txt"):
    key = f.read().strip()
    naturalLanguageUnderstanding = NaturalLanguageUnderstandingV1(
            version='2018-11-16', iam_apikey=key)
### use watson_florida.txt for florida

#for communication with other programs
import time
import socket
import client
import wave
import piimages_final
#import nerf_and_head
import locomotion
import strongarm

#for voice recognition/part of speech parser
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sid
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

#for threading with GUI
from threading import Lock, Thread
import threading
lock = Lock()
lock2 = Lock()

#key constants
setup_bool = False
confirmation_final = 1000
no_clue_final = 999
wakeup_final = 998
sleep_final = 997
move_final = 996
attendance_final = 995
sentiment_value = 0
device_index = 1

"""
THE FUNCTIONS BELOW ARE USED SPECIFICALLY FOR 
VOICE RECOGNITION (DIRECTION OF ARRIVAL AND PRECISION RECOGNITION)
"""
def chunkify(arr):
    acc_total = []
    acc_chunk = np.zeros(8192, dtype='int16')
    i = 0
    for byte in arr:
        if (i < 8192):
            acc_chunk[i] = byte
            i += 1
        else:
            acc_total.append(acc_chunk)
            acc_chunk = np.zeros(8192, dtype='int16')
            i = 0

    return acc_total


def get_direction(buf):
    SOUND_SPEED = 343.2

    MIC_DISTANCE_4 = 0.08127
    MAX_TDOA_4 = MIC_DISTANCE_4 / float(SOUND_SPEED)

    best_guess = None
    MIC_GROUP_N = 2
    MIC_GROUP = [[0, 2], [1, 3]]

    tau = [0] * MIC_GROUP_N
    theta = [0] * MIC_GROUP_N
    for i, v in enumerate(MIC_GROUP):
        tau[i], _ = gcc_phat(buf[v[0]::4], buf[v[1]::4],
                             fs=16000, max_tau=MAX_TDOA_4, interp=1)
        theta[i] = math.asin(tau[i] / MAX_TDOA_4) * 180 / math.pi

        if np.abs(theta[0]) < np.abs(theta[1]):
            if theta[1] > 0:
                best_guess = (theta[0] + 360) % 360
            else:
                best_guess = (180 - theta[0])
        else:
            if theta[0] < 0:
                best_guess = (theta[1] + 360) % 360
            else:
                best_guess = (180 - theta[1])

            best_guess = (best_guess + 90 + 180) % 360

        best_guess = (-best_guess + 120) % 360

    return best_guess


def avg_direction(chunks):
    acc = 0
    i = 0
    dir_chunks = []
    for chunk in chunks:
        direction = get_direction(chunk)
        acc += direction
        i += 1
        dir_chunks.append(direction)

    return (acc/i, dir_chunks)


def remove_outliers(directions, avg_dir):
    res = []
    for direction in directions:
        if (abs(direction - avg_dir) <= 60):
            res.append(direction)

    return res


def avg_list(lst):
    acc = 0
    i = 0

    if (lst == []):
        return 0

    else:
        for elt in lst:
            acc += elt
            i += 1

        return acc/i

"""
listen to user statement in mic
returns spoken words from user OR 
returns empty string if source not detected
"""
def listen(r, mic):
	with mic as source:
		r.adjust_for_ambient_noise(source)
		print("\n\n\nYou may begin talking:\n\n\n") #testing
		audio = r.listen(source)
		byte_data = audio.get_raw_data(16000, 2)
		byte_arr = np.frombuffer(byte_data, dtype='int16')
		chunks = chunkify(byte_arr)
		tup = avg_direction(chunks)
		avg_dir = tup[0]
		directions = remove_outliers(tup[1], avg_dir)
		print("dir w/o removing outliers: " + str(int(avg_dir)))
		if (not(directions == [])):
		    print("dir w/ removing outliers: " + str(int(avg_list(directions))))
		else:
		    print("no outliers to remove: " + str(int(avg_dir)))

	try:
		return r.recognize_google(audio)

	except sr.UnknownValueError:
		print ("What are you saying?") #testing
		return ""
	
"""
plays respective sound from speakers
based on sentiment analysis value
"""
def react_with_sound (sentiment_value):
	
	print ("about to play sound...")
	
	lead_folder = "/home/pi/Desktop/r2-tablet_GUI/R2FinalSounds/"
	sounds = {"confirmation":"R2OK.wav" , "wake up":"R2Awake.wav" , "angry":"R2Angry.wav" , "good":"R2Good.wav" , \
	"happy":"R2Happy.wav" , "neutral":"R2Neutral.wav" , "sad":"R2Sad.wav" , \
	"sleep":"R2Sleep.wav", "no clue":"R2Confused.wav" , "move":"R2Move.wav" , \
	"attendance":"R2Attendance.wav"}
	
	if (sentiment_value == confirmation_final):
		play_sound(lead_folder + sounds["confirmation"])
	elif (sentiment_value == no_clue_final):
		play_sound(lead_folder + sounds["no clue"])
	elif (sentiment_value == wakeup_final):
		play_sound(lead_folder + sounds["wake up"])
	elif (sentiment_value == sleep_final):
		play_sound(lead_folder + sounds["sleep"])
	elif (sentiment_value == move_final):
		play_sound(lead_folder + sounds["move"])
	elif (sentiment_value == attendance_final):
		play_sound(lead_folder + sounds["attendance"])
	elif (sentiment_value < -0.5):
		play_sound(lead_folder + sounds["angry"])
	elif (sentiment_value < 0):
		play_sound(lead_folder + sounds["sad"])
	elif (sentiment_value == 0):
		play_sound(lead_folder + sounds["neutral"])
	elif (sentiment_value > 0.5):
		play_sound(lead_folder + sounds["happy"])
	else:
		play_sound(lead_folder + sounds["good"])

"""
play sounds from speaker
"""
def play_sound(file_name):
	wave_obj = sa.WaveObject.from_wave_file(file_name)
	play_obj = wave_obj.play()
	play_obj.wait_done()
	
"""
invocation used to tell r2 to stop
emergency or intentional
"""
def stop():
	print ("emergency invoked")
	
	# start exit procedure here

	react_with_sound(sleep_final)
	sys.exit()

"""
helper method for r2 to move with xbox controls
"""
def move():
	print ("moving")
	
	#IMPLEMENT HERE
	locomotion.control()
	return 0
	
"""
invokes code for r2 to wave
"""
def wave(methodcnt): # NOTE - INSTANTIATE WITH SPECIAL CASE
	print ("waving")
	
	#implement code here
	strongarm.lift()
	
	return 1

"""
invokes code for r2 to greet people with sound and wave
"""
def greet(methodcnt):
	print ("greeting, don't forget to wave")
	wave(methodcnt)
	react_with_sound(0.6)
	return 2

"""
have r2 take attendance for the lab
"""
def take_attendance(methodcnt):
	print ("checking in - F.R.")
	#react_with_sound(attendance_final)
	client.CheckIn()	
	return 3

"""
have r2 add someone new to its attendance list
"""
def make_friends(name):
	friend = name[len("call me "):] #index where the first name appears
	client.MakeFriend(friend)
	return 4
	
"""
have r2 display what it sees into gui
"""
def object_detection():
	piimages_final.main()
	return 5

"""
have r2 deploy/grab certain item
"""
def grab_item(item, methodcnt):
	if (item == "periscope"):
		open_periscope()
	elif (item == "nerf" or "gun" in item):
		show_guns()
	else:
		print ("grabbing " + item)
		
		#implement grabbing object here
		strongarm.lift()
		
		react_with_sound (confirmation_final)
	return 3

"""
deploy the periscope
"""
def open_periscope():
	print ("opening periscope")
	
	#implement code here
	
	return 4

"""
deploys the nerf guns
"""
def show_guns():
	print ("showing off dem guns...")
	
	#implement code here
	#nerf_and_head.run_nerf_gun()
	return 5

"""
responds to a user's sentiment given a phrase user utters
"""
def sentiment(input):
	try:				
		response = naturalLanguageUnderstanding.analyze(
		text=input,
		features=Features(
		sentiment=SentimentOptions(document=None, targets=None))).get_result()

		parsed_json = json.loads(json.dumps(response, indent=2))
		sentiment = parsed_json['sentiment']
		document = sentiment['document']
		score = document['score']
		sentiment_value = float(score)
			
	except:
		sentiment_value = sid().polarity_scores(input)['compound']
			
	print(sentiment_value)	
	react_with_sound(sentiment_value)
	return 6

"""
write to files that will output to gui
"""
def writeToVoice(input):
	lock.acquire()
	file=open('VoiceRecognitionText.txt','w+')
	file.write(input + "\r\n")
	file.close()	
	lock.release()

"""
write to files that will output to gui
"""
def writeToSentiment(score):
	lock2.acquire()
	score1 = str(score)
	file=open('SentimentAnalysisOutput.txt','w+')
	file.write(score1 + "\r\n")
	file.close()	
	lock2.release()    

def main():
	
	methodcnt = False
	
	# method dispatcher to connect to functions (https://www.reddit.com/r/Python/comments/7udbs1/using_python_dict_to_call_functions_based_on_user/)
	dispatcher = {'wave1':wave, 'greet1':greet, 'take_attendance1':take_attendance, 'grab_item1':grab_item}
	
	# test run to see if all r2 functionality working as expected
	fndictGreetingsKeys = {"wave", "hello", "hi", "hey", "check", "attendance"}
	fndictGetItemsKeys = {"water", "bottle", "stickers", "periscope", "nerf", "guns", "gun"} # NEED TO CHECK SPELLING OF PERISCOPE FOR VOICE RECOGNITION
	
	# in formation of dictionaries, all functions being called
	fndictGreetings = {"wave":dispatcher['wave1'], "hello":dispatcher['greet1'], "hi":dispatcher['greet1'], "hey":dispatcher['greet1'], "check":dispatcher['take_attendance1'], "attendance":dispatcher['take_attendance1']}
	fndictGetItems = {"water":dispatcher['grab_item1'], "bottle":dispatcher['grab_item1'], "stickers":dispatcher['grab_item1'], "periscope":dispatcher['grab_item1'], "nerf":dispatcher['grab_item1'], "guns":dispatcher['grab_item1'], "gun":dispatcher['grab_item1']}
	methodcnt = True
	setup_bool = True
	
	# opens microphone instance that takes speech from human to convert to text
	r = sr.Recognizer()
	mic = sr.Microphone(device_index)
	r.dynamic_energy_threshold = True
	
	# tells R2 to wake up
	while (True):
		spoken = listen(r, mic)
		spoken = spoken_text.lower()
		print("The following startup phrase was said:\n" + spoken + "\n")
		
		close_enough = ["ar2", "or to blue", "hey arthur", "ai2", "they are two", "ko2", 
		"halo 2", "naruto", "ar jail", "ar-10", "airtel", "rdr2 hello", "q38", "hey r2",
		"yo are two", "zr2", "you are two", "hey or two", "hey are two"]
		
		# R2 unsure of input
		if (spoken == ""):
			print ("What?")
			react_with_sound(no_clue_final)
		
		elif ("r2 stop" in spoken):
			stop()
		
		elif (spoken in close_enough):
			print ("awake")
			react_with_sound(wakeup_final)
			break	
			
	# R2 waits to hear what user wants - CHANGE PROMPTS HERE
	while (True):
		
		spoken = listen(r, mic)
		spoken = spoken_text.lower()
		print("The following text was said:\n" + spoken + "\n")
		
		if ("r2 stop" in spoken):
			stop()
		
		# R2 unsure of input
		elif (spoken == ""):
			print ("What?")
			react_with_sound(no_clue_final)
		
		elif ("lift" in spoken):
			wave()
		
		#calling object detection
		elif ("what do you see" in spoken):
			object_detection()
		
		#calling make friends
		elif ("call me " in spoken):
			make_friends(spoken)
		
		else: 
			# use NLTK to determine part of speech of first word spoken
			tokens = nltk.word_tokenize (spoken)
			tagged = nltk.pos_tag(tokens)
			print (tagged[0])
			
			#obtain keywords from uttered phrase
			keywords = liteClient.getKeywords(spoken)
				
			# run through commands first
			if ("wave" in spoken or "high five" in spoken or "VB" in tagged[0] or "JJ" in tagged[0]):
				
				if ("high five" in spoken):
					keywords.append("high five") #need to add a case for r2 to give a high five to user
					
				else:
					for x in range(0, len(keywords)):
							
						word = keywords[x]
						print (word)
							
						react_with_sound (confirmation_final)
								
						if (word in fndictGreetingsKeys):	
							print(fndictGreetings[word](methodcnt))
							print ("in fndictGreetingKeys")
							break
						
						elif (word in fndictGetItemsKeys):
							print(fndictGetItems[word](word, methodcnt))
							print ("in fndictGetItemsKey")
							break
			
			# sentiment analysis
			else:				
				try:				
					global sentiment_value
					response = naturalLanguageUnderstanding.analyze(
					text=spoken,
					features=Features(
					sentiment=SentimentOptions(document=None, targets=None))).get_result()

					parsed_json = json.loads(json.dumps(response, indent=2))
					sentiment = parsed_json['sentiment']
					document = sentiment['document']
					score = document['score']
					sentiment_value = float(score)
					
				except:
					sentiment_value = sid().polarity_scores(spoken)['compound']
				
					
				print(sentiment_value)	
				react_with_sound(sentiment_value)
		
		#writing outcome to gui
		t1 = threading.Thread(target = writeToVoice, args=(spoken,))
		t2 = threading.Thread(target = writeToSentiment, args=(sentiment_value,))
		t1.start()
		t2.start()
		t1.join()
		t2.join()
			
#main() ### COMMENT THIS OUT WHEN MERGING WITH TABLET

