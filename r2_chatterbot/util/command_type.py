import string
import time
from quantulum3 import parser

import nlp_util
import path_planning

# Facial Recognition
def isFaceRecognition(text):
    """
    Determines whether a string is a facial recongnition command. The different
    types of facial recognition commands include greetings, such as "hi," "hello,"
    or "wave," the make new friends command in the form of "call me [name]," or
    attendance command, such as "take attendance."

    @param text: The sentence to check
    @return: A boolean. True indicates that the input a facial recognition command
    """
    keywords_greetings = {"wave ", "hello ", "hi ", "check ", "attendance ", "call me ", "greetings ", "what's up " }
    for item in keywords_greetings:
        if item in text.lower():
            print("item returned: ", item)
            return True
    return False

# Path Planning
directions = path_planning.directions
directions_obstacles = path_planning.directions_obstacles
little = path_planning.little
commands = path_planning.commands
custom_tags = path_planning.custom_tags
custom_tags_obstacle = path_planning.custom_tags_obstacle

def get_locphrase(text):
    """
    Returns a list of tagged phrases that match certain regex chunks corresponding to
    different types of path planning commands.
    @param text: the original text (must be in lowercase)
    """
    # expr = ["DirectionFirst: {(((<TO|IN>)<DT>)?<D><CD><NNS|NN|JJ>?)}",
    #         "NumberFirst: {(<CD><NNS|NN|JJ>?((<TO|IN>)<DT>)?<D>)}",
    #         "LittleDirection: {(((<TO|IN>)<DT>)?<D><A><NNS|NN|JJ>?<NN>?)}",
    #         "LittleNumber: {(<A><NNS|NN|JJ>?<NN>?((<TO|IN>)<DT>)?<D>)}",
    #         "Obstacle: {(((<TO|IN>)<DT>)?<D>)}"
    #         ]
    expr = ["DirectionFirst: {(((<TO|IN>)<DT>)?<D><CD><NNS|NN|JJ>?)}",
            "NumberFirst: {(<CD><NNS|NN|JJ>?((<TO|IN>)<DT>)?<D>)}",
            "LittleDirection: {(((<TO|IN>)<DT>)?<D><A><NNS|NN|JJ>?<NN>?)}",
            "LittleNumber: {(<A><NNS|NN|JJ>?<NN>?((<TO|IN>)<DT>)?<D>)}"]
    locPhrase, keywords = nlp_util.match_regex_and_keywords_pp(text, expr, custom_tags=custom_tags)

    # if len(locPhrase) <= 0 or locPhrase[0].label() == "S":
    #     # didn't get a match before, try only looking for obstacle commands
    #     expr_obstacle = ["Obstacle: {(((<TO|IN>)<DT>)?<D>)}"]
    #     locPhrase, keywords = nlp_util.match_regex_and_keywords_pp(
    #         text, expr_obstacle, custom_tags=custom_tags_obstacle)
    print(locPhrase)
    return locPhrase, keywords

def preprocess(text):
    # removes punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    text = text.replace("seats", "feet")
    text = text.replace("seat", "feet")
    text = text.replace(u"°", " degrees")
    text = text.replace("one", "1")
    text = text.lstrip()
    quant = parser.parse(text)
    for q in quant:
        text_to_replace = parser.inline_parse_and_expand(str(q.value))
        text_to_replace = text_to_replace.replace("-", " ")
        number = int(q.value)
        text = text.replace(text_to_replace, str(number))
    return text


def contains_a_word_in(text_list, search_words):
    """
    Returns true if at least one of the words in search_words is contained in text_list
    """
    return any(word in text_list for word in search_words)

def isLocCommand(text):
    '''
    Determines whether a string is a locomation command or not based on the
    sentence structure.
    @param text: The sentence to check (must be in lowercase)
    @return: A boolean. True indicates that the input is a locomotion command
    '''

    if text == "stop":
        return True
    text = preprocess(text)
    # print("Text: ", text)
    locPhrase, _ = get_locphrase(text)
    # print(locPhrase)

    target_verbs = ["move", "spin", "rotate",
                    "turn", "go", "drive", "stop", "travel"]

    phrases = len(locPhrase)

    # 'S' means we essentially got garbage
    if phrases > 0 and locPhrase[0].label() != 'S':
        for phrase in locPhrase:
            words_only = [x[0] for x in phrase.leaves()]
            if phrase.label() == "Obstacle":
                if phrases > 1:
                    return False  # no more than 1 of this type of phrase
                if contains_a_word_in(text, ["turn", "spin", "rotate"]):
                    return False  # turning commands can't be used with this type
            # if it fell under the little bit phrase, check if one of the little bit words is there
            elif phrase.label() == "LittleDirection" or phrase.label() == "LittleNumber":
                if not contains_a_word_in(words_only, little):
                    return False
            # if it's an obstacle command
        for verb in target_verbs:
            if verb in text:
                return True
    return False


# Object Detection
custom = [("pick", "VB")]

def isObjCommand(text):
    '''
    Determines whether a string is an object detection command or not based on the
    sentence structure

    @param text: The sentence to check (must be in lowercase) Some examples of phrases
    include "grab the watter bottle" or "pick up the pen"
    @return: A boolean. True indicates that the input is an object detection command
    '''
    r_expr = r"""
    VP: {<VB.*>(<RP>)?(<DT>|<PRP.*>)?(<NN>)+}
    """
    target_verbs = ["grab", "get", "take", "pick"]

    verbPhrase, keywords = nlp_util.match_regex_and_keywords(text, r_expr, keywords=target_verbs, custom_tags=custom)
    if len(verbPhrase) > 0 and verbPhrase[0].label() != 'S':
        return True
    else:
        return False

def getCommandType(speech):
    before = time.time()
    if isFaceRecognition(speech):
        response = 'facial recognition'
    elif isLocCommand(speech):
        response = 'path planning'
    elif isObjCommand(speech):
        response = 'object detection'
    else:
        response = 'not a command'
    after = time.time()
    print("Time: ", after - before)
    return response

if __name__ == "__main__":
    print(getInputType('hi '))
    print(getInputType('move five feet forward'))
    print(getInputType('pick up a ball'))
    print(getInputType('this is good'))