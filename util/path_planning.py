import utils
import re
import nlp_util

def isLocCommand(text):
    '''
    Determines whether a string is a locomation command or not based on the
    sentence structure
    @param text: The sentence to check (must be in lowercase)
    @return: A boolean. True indicates that the input is a locomotion command
    '''

    r_expr = r"""
    VP: {<NNP|VB.*|NN><CD|RB|NNS|VBD|JJ><CD|RB|NNS|VBD>(<NNS|RB|VBD>)?}
    """
    target_verbs = ["turn", "move", "go", "spin", "rotate", "twirl"]

    verbPhrase, keywords = nlp_util.match_regex_and_keywords(text, r_expr, target_verbs)
    if len(verbPhrase) > 0:
        return True
    else:
        return False



def pathPlanning(text):
    '''
    This function uses regular expressions to determine whether the input is
    a locomotion command and uses regular expressions to parse the necessary
    data from the inputed text.

    @param text: The sentence to check if it is a locomotion command and
    parse the direction and distance from it. ***MUST BE IN LOWERCASE***
    @return: A tuple. First element is the direction (i.e. 90 if right, 0
    if forward, -90 if left, or 180 of backwards). The second element is the
    distance. If the input text is not a locomation command, the function returns
    (-500, -500) by default.
    '''
    #return variables
    direction = 0
    moveAmmount = 0
    target_directions = ["forward", "backward", "left", "right", "up", "down", "forwards", "backwards"]
    #if we find a path related phrase
    if isLocCommand(text):
        ammountE = r"""
        RB: {<CD>}
        """
        #grabs the number of steps from the phrase
        movePhrase, keyword = nlp_util.match_regex_and_keywords(text, ammountE)
        firstItem = movePhrase[0]
        temp = firstItem[0]
        moveAmmount = temp[0]

        #based on the direction, returns the corresponding degrees
        if "left" in text:
            direction = -90
        if "right" in text:
            direction = 90
        if "forward" in text or "up" in text:
            direction = 0
        if "backward" in text or "down" in text:
            direction = 180
    else:
        direction = -500
        moveAmmount = -500


    return(direction, moveAmmount)

if __name__ == "__main__":
    phrase = "turn right 30 degrees"
    phrase2 = "robot go vroom"
    with open("tests/isLoc.txt") as f:
        for line in f:
            print(line)
            print(pathPlanning(line))
    #print(isLocCommand(phrase))
    #pathPlanning(phrase)
