import utils
import re
import nlp_util
from util import live_streaming

def isFaceRecognition(text):
    """
    C1C0, take attendence -> output a new file with attendence
    C1C0, call me [name] -> output a new file with person's named
    C1C0, greetings
    """
    keywords_greetings = {"wave", "hello", "hi", "hey", "check", "attendance", "call me"}
    for item in keywords_greetings:
        if item in text:
            return True
    return False
def faceRecog(text):
    if isFaceRecognition(text):
        if "attendence" in text:
            live_streaming.append_to_file("attendence.txt", "attendence")
        if "greetings" in text:
            live_streaming.append_to_file("attendence.txt", "attendence")
        if("call me") in text:
            r"""
            nameE: {(<NNP>)+}
            """
            locPhrase= nlp_util.match_regex_and_keywords(text, nameE)

if __name__ == "__main__":
    phrase = "C1C0, move forward 10 steps"
    phrase2 = "robot go vroom"
    with open("tests/isLoc.txt") as f:
        for line in f:
            print(line)
            print(isLocCommand(line))
            print(pathPlanning(line))
    # print(pathPlanning(phrase))
    # print(isLocCommand(phrase))
