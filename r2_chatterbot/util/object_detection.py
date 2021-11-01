import utils
import re
import nlp_util
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

def object_parse(text):
    '''
    This function uses regular expressions to determine whether the input is
    an object detection command and uses regular expressions to parse the necessary
    data from the inputed text.

    @param text: The sentence to check if it is an object detection command.
    ***MUST BE IN LOWERCASE***
    @return: A string depecting what the object is to be picked up. If the o
    object contains a descriptor or is two words, the program will return
    the whole thing. If the input text is not a locomation command, the function
    returns an empty string.
    '''

    item = ""
    itemExp = r"""
    RB: {(<NN>)+}
    """
    if isObjCommand(text):
        locItem = nlp_util.match_regex_and_keywords(text, itemExp, custom_tags=custom)
        firstItem = locItem[0]
        nounsList = firstItem[0]
        for noun in nounsList:
            item = item + noun[0] + " "
    item = item.strip()
    with open("util/coco.txt") as f:
        for line in f:
            if item in line:
                return item
    return None

if __name__ == "__main__":
    phrase = "pick up my umbrella"
    phrase2 = "take 2 steps forward"
    print(isObjCommand(phrase))
    print(object_parse(phrase))
