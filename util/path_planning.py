import utils
import re
import nlp_util

def pathPlanning(text):
    direction = 0
    moveAmmount = 0
    r_expr = r"""
    VP: {<NNP|VB.*|NN><CD|RB|NNS|VBD|JJ><CD|RB|NNS|VBD>(<NNS|RB|VBD>)?}
    """
    target_verbs = ["turn", "move", "go", "spin", "rotate", "twirl"]
    target_directions = ["forward", "backward", "left", "right", "up", "down", "forwards", "backwards"]

    verbPhrase, keywords = nlp_util.match_regex_and_keywords(text, r_expr, target_verbs)
    #print(verbPhrase)

    #if we find a path related phrase
    if len(verbPhrase) > 0:
        ammountE = r"""
        RB: {<CD>}
        """
        #grabs the number of steps from the phrase
        moveAmmount, keyword = nlp_util.match_regex_and_keywords(text, ammountE)

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
    phrase = "move forward 10 steps"
    pathPlanning(phrase)
