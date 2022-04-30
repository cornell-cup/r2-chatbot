from util.small_talk.phatics import get_category, get_response_combined
import utils
import re
import nlp_util
import live_streaming
import os
from small_talk import * 

def isFaceRecognition(text):
    """
    Determines whether a string is a facial recongnition command. The different
    types of facial recognition commands include greetings, such as "hi," "hello,"
    or "wave," the make new friends command in the form of "call me [name]," or
    attendance command, such as "take attendance."

    @param text: The sentence to check
    @return: A boolean. True indicates that the input a facial recognition command
    """
    
    if len(text.strip()) == 0 :
        return (True,'greeting') 

    keywords_greetings = {"hello ", "hi ", "check ", "greetings ", "what's up " }
    #print(text)
    text = text.lower()
    for item in keywords_greetings:
        if item in text and item != "attendance" and item != "wave" and item != "call me":
            return (True,'greeting')
    if "attendance" in text:
        return (True,"attendance")
    elif "call me" in text or "callme" in text:
        return (True,"call")
    if "wave" in text:
        return (True,"wave")
    
    return (False,None)

def faceRecog(text):
    """
    This function takes a text input and determines which facial recognition
    command it is. It also appends the name of the command to a new file. If it
    is a make friends command, it will append the name of the new friend to a
    file.

    @param text: The sentence to check
    @return: A new file with the command name listed.
    """
    greetings_keywords = {"wave ", "hello ", "hi ", "greetings ", "what's up ","Wave ", "Hello ", "Hi ", "Greetings ", "What's up "}
    known = isFaceRecognition(text)
    if known[0]:
        if known[1] == "attendance":
            #implement when chris is done with everything
            return " attendance "

        if known[1] == "greeting":
            return get_response_combined(text,"Chris")

        if known[1] == "call":
            name = ""
            nameE = r"""
            nameE: {(<NNP>)+}
            """
            namePhrase = nlp_util.match_regex_and_keywords(text, nameE)
            nameList = namePhrase[0][0]
            for noun in nameList:
                name = name + noun[0] + " "
            live_streaming.append_to_file("friends.txt", name)
            print("created new attendance file with " + name)


if __name__ == "__main__":
   
    #phrase2 = "robot go vroom"
    #phrase = " "
    #faceRecog(phrase)
    # with open("tests/isLoc.txt") as f:
    #     for line in f:
    #         print(line)
    #         print(isLocCommand(line))
    #         print(pathPlanning(line))
    # print(pathPlanning(phrase))
    # print(isLocCommand(phrase))
