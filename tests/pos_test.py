import sys
import os
sys.path.insert(1, os.path.join(os.getcwd(), ""))
#print(sys.path)

import re
import nltk

from util import detect_question

lines = [
    #need to use a possesive determiner
    #"what's the weather",
    #"what is today's weather",
    #"what is the weather today",
    #"what is the weather like today",

    #"his car is actually his mom's car",
    #"his car is actually his mom's",
    #"his car seat is actually his mom's car seat"
    #"Mary saw the cat sit on the mat"
]
with open("tests/question_keyword_tests.txt") as f:
    for line in f:
        lines.append(line)

expression = r"""
POS_DT: {<NN.*><POS><NN.*>*}
NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
"""
'''
expression = r"""
    NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
    PP: {<IN><NP>}               # Chunk prepositions followed by NP
    VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
"""
'''

for line in lines:
    #break sentence into tokens (ex: words)
    tokenized_line = nltk.word_tokenize(line)

    #mark tokens with part of speech
    pos_tagged = nltk.pos_tag(tokenized_line)

    #the type of phrase we want to detect in a sentence
    parser = nltk.RegexpParser(expression)

    #look through the tagged tokens for the phrase
    parsed_text = parser.parse(pos_tagged)

    #print(parsed_text)
    #parsed_text.draw()

    print(detect_question.match_regex_and_keywords(line, expression,
        ["weather", "temperature", "tomorrow", "today"]))
