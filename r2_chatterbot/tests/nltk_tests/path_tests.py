import sys
import os
import nltk
sys.path.insert(1, os.path.join(os.getcwd(), ""))

lines = []
# with open("restaurant_question_test.txt") as f:
#     for line in f:
#         lines.append(line)

lines = [
    "call me Mrs. Murugesan"
]

# <JJ.*>|<VB.*>|<INRB.*>|

r_expr = r"""
KEYWORDS: {}
DESCRIPTION: {(<NNP>)+}
"""


for line in lines:
    # break sentence into tokens (ex: words)
    tokenized_line = nltk.word_tokenize(line)

    # mark tokens with part of speech
    pos_tagged = nltk.pos_tag(tokenized_line)

    # print(pos_tagged)

    # the type of phrase we want to detect in a sentence
    parser = nltk.RegexpParser(r_expr)

    # look through the tagged tokens for the phrase
    parsed_text = parser.parse(pos_tagged)

    print(parsed_text.draw())
