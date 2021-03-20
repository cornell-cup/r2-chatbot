import re
import nlp_util
import nltk
import math
import string
from quantulum3 import parser


custom_tags = [("forward", "D"), ("forwards", "D"), ("backward", "D"), ("backwards", "D"),
("back", "D"), ("left", "D"), ("right", "D"), ("clockwise", "D"), ("counterclockwise", "D")]

LITTLE_BIT_TURN = 30
LITTLE_BIT_MOVE = 1

def preprocess(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.replace("seats", "feet")
    text = text.replace("seat", "feet")
    text = text.replace(u"°", " degrees")
    text = text.lstrip()
    return text


def get_locphrase(text):
    print("Beginning text:", text)
    """
    Returns the same text, with all numbers converted from English words to
    decimal form.
    Ex. "move five feet forward" returns "move 5 feet forward"

    @param text: the original text (must be in lowercase)
    """
    quant = parser.parse(text)
    for q in quant:
        words = str(q).split(' ')
        number_word = words[0]
        number = int(q.value)
        text = text.replace(number_word, str(number))
    lst = text.split(' ', 1)
    text = text if len(lst) <= 1 else lst[1]
    print("Preprocessed text:", text)
    r_expr2 = r"""
    DirectionFirst: {(((<TO|IN>)<DT>)?<RB|VBD|JJ|VBP|NN|VBN><CD><NNS|NN|JJ>?)}
    NumberFirst: {(<CD><NNS|NN|JJ>?((<TO|IN>)<DT>)?<RB|VBD|JJ|VBP|NN|VBN>)}
    """
    target_verbs = ["move", "spin", "rotate",
                    "turn", "go", "drive", "stop", "travel"]
    target_words = ["degrees", "left", "right", "forward", "backward",
                    "clockwise", "counterclockwise"]

    locPhrase, keywords = nlp_util.match_regex_and_keywords(
        text, r_expr2, custom_tags, target_words)

    print(locPhrase, keywords)

    return locPhrase, keywords

def get_locphrase_b(text):
    print("Beginning text:", text)
    """
    Returns the same text, with all numbers converted from English words to
    decimal form.
    Ex. "move five feet forward" returns "move 5 feet forward"

    @param text: the original text (must be in lowercase)
    """
    quant = parser.parse(text)
    for q in quant:
        words = str(q).split(' ')
        number_word = words[0]
        number = int(q.value)
        text = text.replace(number_word, str(number))
    lst = text.split(' ', 1)
    text = text if len(lst) <= 1 else lst[1]
    print("Preprocessed text:", text)
    r_expr2 = r"""
    DirectionFirst: {(((<TO|IN>)<DT>)?<D><CD|DT><NNS|NN|JJ>?<NN>?)}
    NumberFirst: {(<CD|DT><NNS|NN|JJ>?<NN>?((<TO|IN>)<DT>)?<D>)}
    """
    target_verbs = ["move", "spin", "rotate",
                    "turn", "go", "drive", "stop", "travel"]
    target_words = ["degrees", "left", "right", "forward", "backward",
                    "clockwise", "counterclockwise", "little", "bit"]

    locPhrase, keywords = nlp_util.match_regex_and_keywords(
        text, r_expr2, custom_tags, target_words)

    print(locPhrase)

    return locPhrase, keywords
    # tokenized_line = nltk.word_tokenize(text)
    # print(tokenized_line)
    #
    # # mark tokens with part of speech
    # pos_tagged = nltk.pos_tag(['a', 'little', 'bit'])
    # print(pos_tagged)

def isLocCommand(text):
    '''
    Determines whether a string is a locomation command or not based on the
    sentence structure. A proper locomotion command includes what part to move,
    how much to move it, and the direction to move it. Without these three, the
    command will not be parsed. Some examples are "Move the body forward 10 steps"
    or "Rotate the precision arm left by 10 degrees"

    @param text: The sentence to check (must be in lowercase)
    @return: A boolean. True indicates that the input is a locomotion command
    '''
    # r_expr = r"""
    # VP: {(<JJ>)?<NN.*>+(<VB.*>)?<RB|VBD|JJ|CD>(<CD|JJ>)?}
    # """

    if text == "stop":
        return True
    text = preprocess(text)
    locPhrase, keywords = get_locphrase_b(text)
    print("aa"+str(locPhrase))

    target_verbs = ["move", "spin", "rotate",
                    "turn", "go", "drive", "stop", "travel"]
    for verb in target_verbs:
        if verb in text and len(locPhrase) > 0:
            return True
    return False


def get_loc_params(phrase):
    string = " ".join([word[0] for word in phrase])
    quant = parser.parse(string)[0]
    unit = quant.unit.name
    number = quant.value
    if phrase.label() == "NumberFirst":
        direction = phrase[-1][0]
    else:
        if unit == "dimensionless":
            direction = phrase[-2][0]
        else:
            direction = phrase[-3][0]
    return int(number), unit, direction

def get_loc_params_b(phrase, mode):
    string = " ".join([word[0] for word in phrase])
    if ('little' in string) or ('bit' in string):
        if phrase.label() == "NumberFirst":
            direction = phrase[-1][0]
        else:
            index = 0
            while phrase[index][1] == 'TO' or phrase[index][1] == 'DT':
                index += 1
            direction = phrase[index][0]
        print("direction",  direction)
        if mode == 1: #direction
            return LITTLE_BIT_TURN, "degrees", direction
        elif mode == 2: #distance
            return LITTLE_BIT_MOVE, "metre", direction
        # print('conversion')
        # number = 0.5
        # unit = "metre"
        # print("label", phrase.label())
        # if phrase.label() == "NumberFirst":
        #     direction = phrase[-1][0]
        # else:
        #     direction = "forward"
        # return number, unit, direction
    else:
        quant = parser.parse(string)[0]
        print("quant: ",quant)
        unit = quant.unit.name
        number = quant.value
        if phrase.label() == "NumberFirst":
            direction = phrase[-1][0]
        else:
            if unit == "dimensionless":
                direction = phrase[-2][0]
            else:
                direction = phrase[-3][0]
        return int(number), unit, direction


def process_loc(text):

    mode = 0  # 0 for garbage, 1 for turn, 2 for move

    text = preprocess(text)
    locPhrase, _ = get_locphrase_b(text)

    # tagged_list = nltk.pos_tag(nltk.word_tokenize(text))
    # verbs_and_nouns = [tup[0]
    #                    for tup in tagged_list if tup[1] == 'NN' or tup[1] == 'VB' or tup[1] == 'VBP']
    # # DEBUG THISSSS
    words = nltk.word_tokenize(text)

    for verb in words:
        if verb == "stop":
            return ("stop", 0)
        elif verb in ["turn", "spin", "rotate"]:
            mode = 1
            break
        elif verb in ["move", "go", "drive", "travel"]:
            mode = 2
            break
    # print(locPhrase)
    if mode == 1:
        print("here"+text)
        number, unit, direction = get_loc_params_b(locPhrase[0], mode)
        print(number)
        if unit == "radian":
            number = number * 180 / math.pi
        if direction == "left" or direction == "counterclockwise":
            number = -1 * number
        return ("turn", number)
    if mode == 2:
        if len(locPhrase) > 1:
            x = 0
            y = 0
            prev_unit = None
            for phrase in locPhrase:
                number, unit, direction = get_loc_params_b(phrase, mode)
                # if the unit isn't provided, assume it's the same
                # as the previous unit - if that's unspecified, assume meters
                if unit == "dimensionless":
                    if prev_unit:
                        unit = prev_unit
                    else:
                        unit = "metre"
                        prev_unit = "unit"
                else:
                    prev_unit = unit
                if unit == "foot":
                    number = number * 0.3048
                if direction == "forward":
                    y += number
                elif direction == "left":
                    x -= number
                elif direction == "right":
                    x += number
                elif direction == "backward":
                    y -= number
            return (float(round(x, 2)), float(round(y, 2)))
        elif len(locPhrase) > 0:
            number, unit, direction = get_loc_params_b(locPhrase[0],mode)
            if unit == "foot":
                number = number * 0.3048
            number = float(round(number, 2))
            if direction == "forward":
                return ("move forward", number)
            elif direction == "left":
                return (-number, 0.0)
            elif direction == "right":
                return (number, 0.0)
            elif direction == "backward":
                return (0.0, -number)
            else:
                return ("unknown", 0)

        # 2. check if turn --> movement
        # 3. check if moving
        # a. check if 2 command --> coordinate
        # b. check if 1 command
        # i. check if forward --> movement
        # ii. check if other dir --> coordinate

    return "Not processed"


if __name__ == "__main__":
    # with open("tests/path_planning_phrases.txt") as f:
    #     for line in f:
    #         if line[0] != "#":
    #             is_command = isLocCommand(line)
    #             if is_command:
    #                 process_loc(line)
                #     print("{} \t {} \t {}".format(
                #         line, is_command, process_loc(line)))
                # else:
                #     print("{} \t {}".format(line, is_command))
                # get_locphrase_b("move to the left a tiny little bit")
    # line = "turn to the left 5 meters"
    line = "move left a bit"
    is_command = isLocCommand(line)
    print(is_command)
    if is_command:
        a = process_loc(line)
        print(a)
