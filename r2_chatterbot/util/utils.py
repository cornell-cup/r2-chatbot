import os

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

