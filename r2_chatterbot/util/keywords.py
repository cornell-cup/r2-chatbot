from inspect import getmembers, isfunction
from rake_nltk import Rake
#from util import topic_tests
#from util import nlp_util

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


def get_topic(phrase, parse_location=True):
    '''
    Determines the topic of a keyword phrase

    Output is in the following format:
    {
        "test_result": boolean,
        "info": {
            <specific info for each topic, only if test_result is True>
        },
        "name": <name of the matched function>
    }

    @param phrase: the keyword phrase to test
    @param parse_location: whether to set the location in the info field
        of the dictionary. This should be set to False when using
        chatterbot logic adapters since location would otherwise be parsed
        twice.

    @return: the data output of the matched function, including the
            function's name
    '''

    '''
    getmembers() gives you the name of variables/functions and the
    corresponding value of it in the tuple: (name, value)
    '''
    test_funcs = []
    for x in getmembers(topic_tests):
        if(isfunction(x[1])):
            test_funcs.append(x)
        # if (isfunction(x))
    #test_funcs = [x for x in getmembers(topic_tests) if isfunction(x[1])]

    result = None
    for test in test_funcs:
        result = test[1](phrase, parse_location)

        # if topic was matched
        if result["test_result"]:
            #print("matched %s"%(test[0]))
            result["name"] = test[0]
            return result

    # may need for another function
    result["name"] = ""
    return result


def modify_topic_data(data, parse_location=False):
    '''
    Modifies topic data to include more information. Can be used
    if different pieces of info in topic data were excluded in other
    function calls (such as keywords.get_topic() with parse_location
    set to False) and need to be acquired.

    @param data: the return result from get_topic() that needs
        to be modified
    @param parse_location: whether to parse location
    '''
    if parse_location:
        # attempt to find a location
        location = nlp_util.search_for_location(data["text"])
        data["info"]["location"] = {}
        if len(location) > 0:
            data["info"]["location"]["exists"] = True
            data["info"]["location"]["name"] = location
        else:
            data["info"]["location"]["exists"] = False
            data["info"]["location"]["name"] = ""


if __name__ == "__main__":
    #phrase = extract_keywords("what is the weather today")
    #phrase2 = extract_keywords("what is a good restaurant nearby")
    # print(extract_keywords(phrase))
    phrase = "weather in san francisco"
    phrase2 = "how's ithaca new york's weather"
    get_topic(phrase)
    get_topic(phrase2)
    # print(phrase)
