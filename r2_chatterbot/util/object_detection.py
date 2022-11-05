from tkinter.tix import INTEGER
from xmlrpc.client import MAXINT
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import util.utils as utils
import re
import nlp_util
import time

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
    VP: {<VB.*>(<RP>)?(<DT>|<PRP.*>)?(<NN>|<NNS>)+}
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
    RB: {(<NN>|<NNS>)+}
    """
    if isObjCommand(text):
        locItem = nlp_util.match_regex_and_keywords(text, itemExp, custom_tags=custom)
        firstItem = locItem[0]
        nounsList = firstItem[0]
        for noun in nounsList:
            item = item + noun[0] + " "
    else: return None
    item = item.strip()
    dirname = os.path.dirname(__file__)
    coco_filepath = os.path.join(dirname, "coco.txt")
    with open(coco_filepath) as f:
        objects = set([line.strip() for line in f])
        if (item in objects):
            return item
        closest = 15 # longest string in COCO list
        targ = ""
        arr = item.split()
        len_thres = 5
        for object in objects:
            if (len(arr) > 1): # considers only if there are more than 2 words in item
                for s in arr:
                    if (object == s): return object
                    len_dist = abs(len(s) - len(object))
                    if (len_dist > closest or len_dist > len_thres): continue
                    dist = lev_dist_dp(s, object)
                    if (dist < closest):
                        closest = dist
                        targ = object
            object_separated = object.split() # separates the word into 2 words
            if len(object_separated) > 1: # consider a mult-line word
                for s in object_separated:
                    if (item == s): return object
            len_dist = abs(len(item) - len(object))
            if (len_dist > closest or len_dist > len_thres): continue
            dist = lev_dist_dp(item, object)
            if (dist < closest):
                closest = dist
                targ = object
            # may want to take into account separated words (ex: computer keyboard)
        threshold = 5
        if (closest < threshold): return targ
    return None

def lev_dist_dp(item, line):
    '''
    This function determines the edit/Levenshtein distance between item and line 

    @param item, line - string inputs
    @return the edit distance between item and line
    '''

    len1 = len(item)
    len2 = len(line)
    # initialize dist_arr for col 0 and row 0 (each from 0 .. len)
    dist_arr = [[x if y == 0 else y if x == 0 else 0 for x in range(len2+1)] for y in range(len1+1)]
    for it in range(1, len1+1):
        for ln in range(1, len2+1):
            if (item[it-1] == line[ln-1]):
                dist_arr[it][ln] = dist_arr[it-1][ln-1]
            else: dist_arr[it][ln] = 1 + min(dist_arr[it][ln-1], dist_arr[it-1][ln], dist_arr[it-1][ln-1])
    return dist_arr[len1][len2]

if __name__ == "__main__":
    phrases = ["pick up the teddy bear", 
    "pick up the bear", 
    "can you grab the cell phone?", 
    "can you grab the phone?", 
    "get the glasses", 
    "get the eyeglasses", 
    "get the eye glasses", 
    "pick up the ball"]
    for phrase in phrases:
        before = time.time()
        isCommand = isObjCommand(phrase)
        obj = object_parse(phrase)
        after = time.time()
        print(isCommand, obj, f"{after - before} s")
    #phrase = "pick up the toothbrushes please"
    # phrase2 = "pick up the water bottle"
    # print(isObjCommand(phrase2))
    # # print(lev_dist_dp("computer keyboard", "keyboard"))
    # # print(lev_dist_dp("toothbrushes", "toothbrush"))
    # # print(lev_dist_dp("please", "plate"))
    # print(object_parse(phrase2))
