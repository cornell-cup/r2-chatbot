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

def capitalize_all(s):
    words = s.strip().split()

    res = ""
    for w in words:
        res += w.capitalize() + " "
    return res

def set_classpath():
    if "CLASSPATH" not in os.environ:
        os.environ["CLASSPATH"] = ""
    os.environ["CLASSPATH"] += ("%s%s"%(
        os.pathsep,
        os.path.join(
            os.getcwd(), "dep", "stanford-ner", "stanford-ner.jar")))
    print(os.environ["CLASSPATH"])

def filter_cico(line):
    speech = line
    
    # filter out cico since it messes with location detection
    for s in [r"((k|K)((i|1)k(o|0))|((c|C)(i|1)c(o|0)))", r"(h|H)ey"]:
        speech = re.sub(s, "", speech)
    speech = speech.strip(".,?! ")

    return speech

