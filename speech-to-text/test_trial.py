import trial

#Tests the string and confidence levels for R2.wav
print(trial.get_string(trial.convert_to_text("R2.wav",44100)))
print(trial.get_confidence(trial.convert_to_text("R2.wav",44100)))

#Tests the string and confidence levels for r2stop.wav
print(trial.get_string(trial.convert_to_text("r2stop.wav",44100)))
print(trial.get_confidence(trial.convert_to_text("r2stop.wav",44100)))

#Tests the string and confidence levels for thereTheirTesting.wav
print(trial.get_string(trial.convert_to_text("thereTheirTesting.wav",44100)))
print(trial.get_confidence(trial.convert_to_text("thereTheirTesting.wav",44100)))

#Tests the string and confidence levels for uncertainStatement.wav
print(trial.get_string(trial.convert_to_text("uncertainStatement.wav",44100)))
print(trial.get_confidence(trial.convert_to_text("uncertainStatement.wav",44100)))

#Tests the string and confidence levels for weatherQuestion.wav
print(trial.get_string(trial.convert_to_text("weatherQuestion.wav",44100)))
print(trial.get_confidence(trial.convert_to_text("weatherQuestion.wav",44100)))

#Tests the string and confidence levels for sample.wav
print(trial.get_string(trial.convert_to_text("sample.wav",48000)))
print(trial.get_confidence(trial.convert_to_text("sample.wav",48000)))
