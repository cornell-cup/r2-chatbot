import punctuation

print(punctuation.sample_recognize("resources/weatherQuestion.wav"))
print(punctuation.sample_recognize("resources/thereTheirTesting.wav"))#Not good at differentiating between theres
print(punctuation.sample_recognize("resources/uncertainStatement.wav"))
print(punctuation.sample_recognize("resources/excited.wav")) #can't detect exclamation points
print(punctuation.sample_recognize("resources/restaurantQuestion.wav"))
print(punctuation.sample_recognize("resources/homeworkQuestion.wav"))
print(punctuation.sample_recognize("resources/commaTest.wav")) #comma test not working
print(punctuation.sample_recognize("resources/ComeC1C0.wav"))
print(punctuation.sample_recognize("resources/C1C0Stop.wav"))#no punctuation "Chico" instead of C1C0
