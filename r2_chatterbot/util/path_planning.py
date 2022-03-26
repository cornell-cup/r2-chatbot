import re
import nlp_util
import nltk
import math
import string
from quantulum3 import parser


# setup for custom tags

directions = ["forward", "forwards", "backward", "backwards", "back", "left", "right",
              "clockwise", "counterclockwise"]
directions_obstacles = ["forward", "forwards", "backward", "backwards", "back", "left", "right"]
little = ["little", "bit", "smidge", "tiny"]
commands = ["move", "spin", "rotate", "turn", "go", "drive", "stop", "travel"]

custom_tags = [(d, "D") for d in directions] + [(c, "V") for c in commands]
custom_tags.append(("a", "A"))
custom_tags_obstacle = [(d, "D") for d in directions_obstacles] + [(c, "V") for c in commands]
custom_tags_obstacle.append(("a", "A"))

# defining constants for small movements

LITTLE_BIT_TURN = 15
LITTLE_BIT_MOVE = 0.3


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


def test_locphrase(text):
    # experimental function for different regex parsing
    expr = ["DirectionFirst: {(((<TO|IN>)<DT>)?<D><CD><NNS|NN|JJ>?)}",
            "NumberFirst: {(<CD><NNS|NN|JJ>?((<TO|IN>)<DT>)?<D>)}",
            "LittleDirection: {(((<TO|IN>)<DT>)?<D><A><NNS|NN|JJ>?<NN>?)}",
            "LittleNumber: {(<A><NNS|NN|JJ>?<NN>?((<TO|IN>)<DT>)?<D>)}",
            "Obstacle: {(((<TO|IN>)<DT>)?<D>)}"]
    locPhrase, keywords = nlp_util.match_regex_and_keywords_pp(text, expr, custom_tags=custom_tags)
    return locPhrase


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
    return locPhrase, keywords


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


def get_direction(phrase):
    """
    Finds a direction word in a phrase and sets similar direction words to the same direction.
    """
    for i in phrase.leaves():
        if i[1] == 'D':
            direction = i[0]
            if direction in ["forward", "forwards"]:
                return "forward"
            elif direction in ["backward", "backwards", "back"]:
                return "backward"
            else:
                return direction


def get_loc_params(phrase, label, mode=None):
    """
    Returns the number, unit, and direction of one phrase dictating movement based on the phrase
    and the mode (1 for turning, 2 for straight movement)
    """
    string = " ".join([word[0] for word in phrase])
    word_list = [word[0] for word in phrase]
    string = " ".join(word_list)
    if label == "Obstacle":
        unit = -1
        direction = phrase[-1][0]
        return 0, -1, direction
    elif contains_a_word_in(word_list, little):
        # print('conversion! mode: ', mode)
        if mode == 1:
            number = LITTLE_BIT_TURN
            unit = "degrees"
        else:
            number = LITTLE_BIT_MOVE
            unit = "metre"
    elif(parser.parse(string) == []):
        unit = -1
        direction = phrase[-1][0]
        return 0, -1, direction
    else:
        quant = parser.parse(string)[0]
        unit = quant.unit.name
        number = quant.value
    direction = get_direction(phrase)
    return float(number), unit, direction


def process_loc(text):
    """
    Returns a tuple value specifying how CICO should move.
    """

    mode = 0  # 0 for garbage, 1 for turn, 2 for move

    text = preprocess(text)
    locPhrase, _ = get_locphrase(text)

    # tagged_list = nltk.pos_tag(nltk.word_tokenize(text))
    # verbs_and_nouns = [tup[0]
    #                    for tup in tagged_list if tup[1] == 'NN' or tup[1] == 'VB' or tup[1] == 'VBP']
    # TODO: Debug me
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
    if mode == 1:
        number, unit, direction = get_loc_params(
                locPhrase[0], locPhrase[0].label(), mode)
        # print("here"+text)
        # number, unit, direction = get_loc_params_b(locPhrase[0], mode)
        # print(number)
        if unit == "radian":
            number = number * 180 / math.pi
        if direction == "left" or direction == "counterclockwise":
            number = -1 * number
        return ("turn", round(number, 2))
    elif mode == 2:
        if len(locPhrase) > 1:
            x = 0
            y = 0
            prev_unit = None
            for phrase in locPhrase:
                number, unit, direction = get_loc_params(
                    phrase, phrase.label(), mode)
                # number, unit, direction = get_loc_params_b(phrase, mode)
                # if the unit isn't provided, assume it's the same
                # as the previous unit - if that's unspecified, assume meters
                # print(number, unit, direction)
                if unit == "dimensionless":
                    if prev_unit:
                        unit = prev_unit
                    else:
                        unit = "metre"
                        prev_unit = unit
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
                elif direction == "backward" or direction == "backwards":
                    y -= number
            return ("move", (float(round(x, 2)), float(round(y, 2))))
        elif len(locPhrase) > 0:
            number, unit, direction = get_loc_params(
                locPhrase[0], locPhrase[0].label(), mode)
            # number, unit, direction = get_loc_params_b(locPhrase[0],mode)
            if(unit == -1):
                return ("keep moving", direction)
            if unit == "foot":
                number = number * 0.3048
            number = float(round(number, 2))
            if direction == "forward":
                return ("move forward", number)
            elif direction == "left":
                return (-number, 0.0)
            elif direction == "right":
                return (number, 0.0)
            elif direction == "backward" or direction == "backwards":
                return (0.0, -number)
            else:
                return ("unknown", 0)

    return "Not processed"


if __name__ == "__main__":
    while True:
        line = input("Command: ")
        is_command = isLocCommand(line)
        # print(is_command)
        if is_command:
            print(process_loc(line))
