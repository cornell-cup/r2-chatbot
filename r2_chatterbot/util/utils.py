import os
import re

def load_words(filename):
    '''
    Loads words from a text file. The text file must have words on seperate
    lines

    @param filename: the path to the text file

    @return: a list of extracted words
    '''
    out = []
    with open(filename) as f:
        for line in f:
            out.append(line.strip())

    return out

def set_classpath():
    '''
    Sets the CLASSPATH environment variable to point to the Stanford
    NER Tagger jar file.
    '''
    
    if "CLASSPATH" not in os.environ:
        os.environ["CLASSPATH"] = ""
    os.environ["CLASSPATH"] += ("%s%s"%(
        os.pathsep,
        os.path.join(
            os.getcwd(), "dep", "stanford-ner", "stanford-ner.jar")))
    print(os.environ["CLASSPATH"])

def filter_cico(line):
    '''
    Removes any instance of "c1c0" (and other variants) from the string.
    Also filters out the word "hey" and strips some punctation/whitespace.
    
    @param line: the string to filter

    @return: a new string with the filtered line
    '''
    speech = line
    
    for s in [r"((k|K)((i|1)k(o|0))|((c|C)(i|1)c(o|0)))", r"(h|H)ey"]:
        speech = re.sub(s, "", speech)
    
    speech = speech.strip(".,?!")
    speech = speech.strip()

    return speech

