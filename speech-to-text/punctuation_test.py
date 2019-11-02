import punctuation

punctuation.sample_recognize("resources/weatherQuestion.wav")
punctuation.sample_recognize("resources/thereTheirTesting.wav")#Not good at differentiating between theres
punctuation.sample_recognize("resources/uncertainStatement.wav")
punctuation.sample_recognize("resources/excited.wav") #can't detect exclamation points
punctuation.sample_recognize("resources/restaurantQuestion.wav")
punctuation.sample_recognize("resources/homeworkQuestion.wav")
punctuation.sample_recognize("resources/commaTest.wav") #comma test not working
punctuation.sample_recognize("resources/ComeC1C0.wav")
punctuation.sample_recognize("resources/C1C0Stop.wav")#no punctuation "Chico" instead of C1C0
