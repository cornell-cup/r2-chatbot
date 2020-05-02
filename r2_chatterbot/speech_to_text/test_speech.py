import speech


#Tests the string and confidence levels for thereTheirTesting.wav
print(speech.get_string(speech.convert_to_text("thereTheirTesting.wav",44100)))
print(speech.get_confidence(speech.convert_to_text("thereTheirTesting.wav",44100)))

#Tests the string and confidence levels for uncertainStatement.wav
print(speech.get_string(speech.convert_to_text("uncertainStatement.wav",44100)))
print(speech.get_confidence(speech.convert_to_text("uncertainStatement.wav",44100)))

#Tests the string and confidence levels for weatherQuestion.wav
print(speech.get_string(speech.convert_to_text("weatherQuestion.wav",44100)))
print(speech.get_confidence(speech.convert_to_text("weatherQuestion.wav",44100)))

#Tests the string and confidence levels for sample.wav
print(speech.get_string(speech.convert_to_text("sample.wav",48000)))
print(speech.get_confidence(speech.convert_to_text("sample.wav",48000)))
