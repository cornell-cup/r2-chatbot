import utils
import re
import nlp_util

def isObjCommand(text):
    r_expr = r"""
    VP: {<VB.*>(<DT>)?(<NN>)+}
    """
    target_verbs = ["grab", "get", "take", "pick up"]

    verbPhrase, keywords = nlp_util.match_regex_and_keywords(text, r_expr, target_verbs)
    if len(verbPhrase) > 0:
        return True
    else:
        return False

def object_parse(text):
    item = ""
    itemExp = r"""
    RB: {(<NN>)+}
    """
    if isObjCommand(text):
        locItem = nlp_util.match_regex_and_keywords(text, itemExp)
        firstItem = locItem[0]
        nounsList = firstItem[0]
        for noun in nounsList:
            item = item + noun[0] + " "
    return item

if __name__ == "__main__":
    phrase = "pick up the potato"
    phrase2 = "robot go vroom"
    #print(object_parse(phrase))
    with open("tests/is_obj.txt") as f:
        for line in f:
            print(line)
            print(object_parse(line))
