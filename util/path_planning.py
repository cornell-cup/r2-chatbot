import utils
import re
import nlp_util

def isLocCommand(text):
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
    #return variables
    direction = 0
    moveAmmount = 0

    #regular expression that embodies a movePhrase
    r_expr = r"""
    VP: {<NNP|VB.*|NN><CD|RB|NNS|VBD|JJ><CD|RB|NNS|VBD>(<NNS|RB|VBD>)?}
    """
    target_verbs = ["turn", "move", "go", "spin", "rotate", "twirl"]
    target_directions = ["forward", "backward", "left", "right", "up", "down", "forwards", "backwards"]

    verbPhrase = nlp_util.match_regex_and_keywords(text, r_expr, target_verbs)
    #if we find a path related phrase
    if len(verbPhrase) > 0:
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

    print(direction, moveAmmount)

if __name__ == "__main__":
    phrase = "Move 10 steps backwards"
    isLocCommand(phrase)
    pathPlanning(phrase)
