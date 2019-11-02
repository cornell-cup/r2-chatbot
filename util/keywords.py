from inspect import getmembers, isfunction
from rake_nltk import Rake

import topic_tests

r = Rake()

def extract_keywords(text):
    '''
    Finds the highest ranked keyword phrase

    @param text: the text to analyze

    @return: the top ranked keyword phrase that was detected
    '''
    
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()[0]

def get_topic(phrase):
    '''
    Determines the topic of a keyword phrase

    @param phrase: the keyword phrase to test

    @return: the name of the function that was matched (usually the
        name of the topic)
    '''
    
    '''
    getmembers() gives you the name of variables/functions and the
    corresponding value of it in the tuple: (name, value)
    '''
    test_funcs = [x for x in getmembers(topic_tests) if isfunction(x[1])]
    #print(test_funcs)

    for test in test_funcs:
        if test[1](phrase)["test_result"]:
            print("matched %s"%(test[0]))

if __name__ == "__main__":
    phrase = extract_keywords("what is the weather today")
    phrase2 = extract_keywords("what is a good restaurant nearby")
    print(extract_keywords(phrase))
    get_topic(phrase)
    get_topic(phrase2)
    #print(phrase)

