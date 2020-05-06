'''
This file contains functions to test a sentence for certain topics
'''

from util import utils
# import nlp_util
import re
from util import nlp_util

'''
return format for all functions in this module

{
    "test_result": boolean,
    "text": string,
    "info": {
        <specific info for each topic, only if test_result is True>
        "keywords": [
            <string>,
            ...
        ],
        "location": {
            "exists": <boolean>,
            "name": <string>
        }
    }
}
'''
def weather(text, parse_location=True):
    print("weather")
    '''
    Tests if the text is about weather and identifies any time words

    @param text: the text to analyze
    @param parse_location: whether to set the location in the info field
        of the dictionary. This should be set to False when using
        chatterbot logic adapters since location would otherwise be parsed
        twice.

    @return: a dictionary, format is specified at the top of the file
    '''
    output = {
        "test_result": False,
        "text": text,
        "info": {}
    }

    #posessive determiner and noun phrase
    expression = r"""
    NP: {<DT|JJ|NN.*>*<NN.*>}
    POS_DT: {<NN.*><POS><NN.*>*}
    """
    #NP: {<DT|JJ|NN.*>+}

    #the keywords we want to detect
    target_words = utils.load_words("data/weather_topic_words.txt")
    time_words = utils.load_words("data/weather_time_words.txt")

    chunks, keywords = nlp_util.match_regex_and_keywords(
            text, expression, target_words)
    #print(chunks)

    #if we found a weather related phrase
    if len(chunks) > 0:
        output["test_result"] = True
        output["info"]["keywords"] = keywords

        if parse_location:
            #attempt to find a location
            location = nlp_util.search_for_location(text)
            output["info"]["location"] = {}
            if len(location) > 0:
                output["info"]["location"]["exists"] = True
                output["info"]["location"]["name"] = location
            else:
                output["info"]["location"]["exists"] = False
                output["info"]["location"]["name"] = ""

    print(output)
    return output

def restaurant(text, parse_location=True):
    '''
    Checks if the text is about restaurants

    @param text: the text to analyze
    @param parse_location: whether to set the location in the info field
        of the dictionary. This should be set to False when using
        chatterbot logic adapters since location would otherwise be parsed
        twice.

    @return: a dictionary, format is specified at the top of the file
    '''

    output = {
        "test_result": False,
        "text": text,
        "info": {}
    }

    # trying to remove all the non-alphabet characters in the string
    regex = re.compile('([^\s\w]|_)+')
    text = regex.sub('', text)

    target_words = utils.load_words("data/restaurant_topic_words.txt")

    for word in target_words:
        if word =="eat":
            word = " eat"
        if word in text:
            output["test_result"] = True

    if output["test_result"] == False:
        return output
    
    if parse_location:
        #attempt to find a location
        location = nlp_util.search_for_location(text)
        output["info"]["location"] = {}
        if len(location) > 0:
            output["info"]["location"]["exists"] = True
            output["info"]["location"]["name"] = location
        else:
            output["info"]["location"]["exists"] = False
            output["info"]["location"]["name"] = ""

    return output
