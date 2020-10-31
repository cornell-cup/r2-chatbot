import utils
import re
import nlp_util
import nltk
import math


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

    # TODO: Make these include more than just "to the", should also work for "in the"
    r_expr2 = r"""
    NumberFirst: {(<CD><NNS>?(<TO><DT>)?<RB|VBD|JJ|VBP|NN>)}
    DirectionFirst: {((<TO><DT>)?<RB|VBD|JJ|VBP|NN><CD><NNS>?)}
    """
    target_verbs = ["move", "spin", "rotate",
                    "turn", "go", "drive", "stop", "travel"]
    target_words = ["degrees", "left", "right", "forward", "backward",
                    "clockwise", "counterclockwise"]

    locPhrase, keywords = nlp_util.match_regex_and_keywords(
        text, r_expr, target_words)
    for verb in target_verbs:
        if verb in text and len(locPhrase) > 0:
            return True
    return False


def get_loc_params(phrase):
    if locphrase[0].label() == "NumberFirst":
        number = locphrase[0][0]
        unit = locphrase[0][1]
        direction = locphrase[0][-1]
    else:
        direction = locphrase[0][-3]
        number = locphrase[0][-2]
        unit = locphrase[0][-1]
    return number, unit, direction


def process_loc(text):

    mode = 0  # 0 for garbage, 1 for turn, 2 for move

    r_expr2 = r"""
    NumberFirst: {(<CD><NNS>?(<TO><DT>)?<RB|VBD|JJ|VBP|NN>)}
    DirectionFirst: {((<TO><DT>)?<RB|VBD|JJ|VBP|NN><CD><NNS>?)}
    """
    target_verbs = ["move", "spin", "rotate",
                    "turn", "go", "drive", "stop", "travel"]
    target_words = ["degrees", "left", "right", "forward", "backward",
                    "clockwise", "counterclockwise"]

    locPhrase, keywords = nlp_util.match_regex_and_keywords(
        text, r_expr2, target_words)

    tagged_list = nltk.pos_tag(nltk.word_tokenize(text))
    verbs_and_nouns = [tup[0]
                       for tup in tagged_list if tup[1] == 'NN' or tup[1] == 'VB']

    for verb in verbs_and_nouns:
        if verb == "stop":
            return ("stop", 0)
        elif verb in ["turn", "spin", "rotate"]:
            mode = 1
        elif verb in ["move", "go", "drive", "travel"]:
            mode = 2

    if mode == 1:
        number, unit, direction = get_loc_params(locphrase[0])
        if unit == "radian" or "radians":
            number = number * 180 / math.pi
        if direction == "left":
            direction = "counterclockwise"
        elif direction == "right":
            direction = "clockwise"
        # direction: clockwise or counterclockwise, number in degrees
        return (direction, number)

    if mode == 2:
        if len(locphrase) > 1:
            x, y = 0
            for each phrase in locphrase:
                number, unit, direction = get_loc_params(phrase):
                if unit == "feet" or "foot":
                    number = number * 0.3048
                if direction1 == "forward":
                    y += number
                elif direction == "left":
                    x -= number
                elif direction == "right":
                    x += number
                elif direction == "backward":
                    y -= number
            return (x, y)
        else:
            number, unit, direction = get_loc_params(locphrase[0])
            if unit == "feet" or "foot":
                number = number * 0.3048
            if direction == "forward":
                return ("move forward", number)
            elif direction == "left":
                return (-number, 0)
            elif direction == "right":
                return (number, 0)
            elif direction == "backward":
                return (0, -number)
            else:
                return (0, 0)

        # 2. check if turn --> movement
        # 3. check if moving
        # a. check if 2 command --> coordinate
        # b. check if 1 command
        # i. check if forward --> movement
        # ii. check if other dir --> coordinate

    return locPhrase, keywords


def pathPlanning(text):
    '''
    This function uses regular expressions to determine whether the input is
    a locomotion command and uses regular expressions to parse the necessary
    data from the inputed text.

    @param text: The sentence to check if it is a locomotion command and
    parse the direction and distance from it. ***MUST BE IN LOWERCASE***
    @return: A triple. The first element is the body part to move.  Second
    element is the direction (i.e. 90 if right, 0 if forward, -90 if left, or
    180 of backwards). The Third element is the
    distance. If the input text is not a locomation command, the function returns
    ("", -500, -500) by default.
    '''
    # return variables
    direction = -500
    moveAmmount = -500
    itemMove = ""
    target_directions = ["forward", "backward", "left",
                         "right", "up", "down", "forwards", "backwards"]
    target_movements = ["strong arm", "precision arm", "body", "C1C0", "head", "cico",
                        "c1c0", "kiko", "strongarm", "precisionarm", "strong-arm", "precision-arm"]
    # if we find a path related phrase
    if isLocCommand(text):
        ammountE = r"""
        RB: {<CD>}
        """
        # grabs the number of steps from the phrase
        movePhrase, keyword = nlp_util.match_regex_and_keywords(text, ammountE)
        firstItem = movePhrase[0]
        temp = firstItem[0]
        moveAmmount = temp[0]
        for item in target_movements:
            if item in text:
                itemMove = item
        # based on the direction, returns the corresponding degrees
        if "left" in text:
            direction = -90
        if "right" in text:
            direction = 90
        if "forward" in text or "up" in text:
            direction = 0
        if "backward" in text or "down" in text:
            direction = 180

    return(itemMove, direction, moveAmmount)


if __name__ == "__main__":
    phrase = "C1C0, move forward 10 steps"
    phrase2 = "robot go vroom"
    # with open("tests/isLoc.txt") as f:
    #     for line in f:
    #         print(line)
    #         print(isLocCommand(line))
    #         print(pathPlanning(line))
    print(isLocCommand(phrase))
    print(isLocCommand(phrase2))
