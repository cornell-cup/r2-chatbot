import utils
import re
import nlp_util
import live_streaming

def isFaceRecognition(text):
    """
    C1C0, take attendence -> output a new file with attendence
    C1C0, call me [name] -> output a new file with person's named
    C1C0, greetings
    """
    keywords_greetings = {"wave", "hello", "hi", "check", "attendance", "call me", "greetings", "what's up" }
    for item in keywords_greetings:
        if item in text.lower():
            return True
    return False

def faceRecog(text):
    greetings_keywords = {"wave", "hello", "hi", "greetings", "what's up","Wave", "Hello", "Hi", "Greetings", "What's up"}
    if isFaceRecognition(text):
        if "attendance" in text:
            live_streaming.append_to_file("attendance.txt", "attendance")
            print("created new attendance file");
        for greeting in greetings_keywords:
            if greeting in text:
                live_streaming.append_to_file("greeting.txt", "greeting")
                print("created new greetings file");

        if("call me") in text or "Call me" in text:
            name = ""
            nameE = r"""
            nameE: {(<NNP>)+}
            """
            namePhrase = nlp_util.match_regex_and_keywords(text, nameE)
            nameList = namePhrase[0][0]
            for noun in nameList:
                name = name + noun[0] + " "
            live_streaming.append_to_file("friends.txt", name)
            print("created new attendance file with " + name);


if __name__ == "__main__":
    phrase = "take attendance"
    phrase2 = "robot go vroom"
    print(isFaceRecognition(phrase))
    faceRecog(phrase);
    # with open("tests/isLoc.txt") as f:
    #     for line in f:
    #         print(line)
    #         print(isLocCommand(line))
    #         print(pathPlanning(line))
    # print(pathPlanning(phrase))
    # print(isLocCommand(phrase))
