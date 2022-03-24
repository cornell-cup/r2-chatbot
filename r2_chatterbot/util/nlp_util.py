import os
import re  # regex module
import nltk
# from util import utils
import utils
import itertools



def parse(line, expression, custom_tags=[]):
    '''
    Looks for a certain type of phrase for all the sentences in a file
    @param line: The sentence to check
    @param expression: A raw string containing the regular expression
            chunk to match. This is utilizing nltk's regex parser
    @return: The syntax tree representing the parsed sentence
    '''

    try:
        # break sentence into tokens (ex: words)
        tokenized_line = nltk.word_tokenize(line)

        # mark tokens with part of speech
        pos_tagged = nltk.pos_tag(tokenized_line)

        for tag in custom_tags:
            if tag[0] in tokenized_line:
                index = tokenized_line.index(tag[0])
                pos_tagged[index] = tag

        # the type of phrase we want to detect in a sentence
        parser = nltk.RegexpParser(expression)

        # look through the tagged tokens for the phrase
        parsed_text = parser.parse(pos_tagged)

        # print("Parsed text: ", parsed_text)
        # parsed_text.draw()

    except Exception as e:
        print(str(e))
        return None

    return parsed_text


def is_question(line):
    '''
    Checks if a sentence is a question
    @param line: The sentence to check
    @return: List containing boolean saying whether the sentence is a question, and string saying type of question
    '''
    line = utils.filter_cico(line, False)

    question = False
    if '?' in line:
        question = True

    tree = parse(line, r"question: {<W..?>}")

    # if question and tree is None:
    #     return True, "Q/A question"

    if question and len(list(tree.subtrees(filter=lambda tree: tree.label() == "question"))) > 0:
        return True, 'wh question'
    elif question:
        return True, 'yes/no question'
    return False, 'not a question'


def search_for_location(line):
    """
    Verifies if passed in chunks are names of cities/locations
    Assumptions made:
    If the statement is about weather, then all named entities are treated
    as a location (this includes ORGANIZATION, PERSON tags)
    This function utilizes a combination of nltk's built in pos_tag() function and
    the Stanford NER Tagger. The function will choose the option that gives a longer
    location string.
    @param line: the text to search through
    @return: a string of the found location, if none found, returns None
    """
    ner_tagger = nltk.StanfordNERTagger(
        "%s/dep/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz" % (os.getcwd()))

    # tags to identify for nltk
    loc_labels = ["GPE", "ORGANIZATION", "PERSON"]

    tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(line)))
    # tree.draw()
    tags = ner_tagger.tag(line.split())
    # print(tags)

    # figure out the location from the Stanford tagger
    ner_location = ""
    for tag in tags:
        if tag[1] == "LOCATION":
            ner_location += (tag[0] + " ")

    ner_location = ner_location.strip()
    ner_location = ner_location.strip("?!., ")
    print("ner loc: %s" % (ner_location))

    # figure out the location from the nltk tagger
    location = ""

    # only the top level has the "S" label
    for subtree in tree.subtrees(lambda t: t.label() == "S"):
        for chunk in subtree.subtrees(lambda t: t.height() == 2):

            # some "chunks" are just strings apparently
            if isinstance(chunk, str):
                continue

            # each seperate detected word will be seperated with a comma
            if chunk.label() in loc_labels:
                location_elem = ""

                for word, pos in chunk:
                    location_elem += word + " "

                location_elem = location_elem.strip()

                location += location_elem + ", "

    location = location.strip()
    location = location.strip(" ,")
    print("nltk loc: %s" % (location))

    '''
    if location != "":
        print("found location %s"%(location))
    else:
        print("No location found")
    '''

    return location if len(location) > len(ner_location) else ner_location


def match_regex_and_keywords(line, exp, custom_tags=[], keywords=None):
    '''
    Attempts to first match the nltk regular expression to the
    specified sentence. Then, for each matched chunk, determines whether
    any keywords are in the chunk
    @param line: The sentence to check
    @param expression: A raw string containing the regular expression
            chunk to match. This is utilizing nltk's regex parser
    @param keywords: Optional. An array containing keywords to match.
            Can also require keywords to appear only in certain chunks.
    @return: A tuple. First element is a list of matched chunks. If
            keywords was specified, will only return chunks where a
            keyword was contained in it
            Second element is a list of matched keywords. Only use if
            keywords was specified
    '''
    matched_chunks = []
    matched_keywords = []

    tree = parse(line, exp, custom_tags)
    # only loop over full trees, not subtrees or leaves
    # only root node has the "S" label
    for subtree in tree.subtrees(lambda t: t.label() == "S"):

        # now loop through subtrees, detected chunks have height 2
        for chunk in subtree.subtrees(lambda t: t.height() == 2):
            if chunk.label() != "S":
                if keywords == None:
                    # no keyword detection needed
                    matched_chunks.append(chunk)
                else:
                    if chunk != subtree:
                        # the format is (<word>, <pos_tag>) for a single word
                        for word, tag in chunk.leaves():
                            if word in keywords:
                                matched_chunks.append(chunk)
                                matched_keywords.append(word)
                                break

    return (matched_chunks, matched_keywords)


def match_regex_and_keywords_pp(line, exp, custom_tags=[], keywords=None):
    '''
    Attempts to first match the nltk regular expression to the
    specified sentence. Then, for each matched chunk, determines whether
    any keywords are in the chunk

    @param line: The sentence to check
    @param expression: A list containing the regular expressions
            chunk to match. This is utilizing nltk's regex parser
    @param keywords: Optional. An array containing keywords to match.
            Can also require keywords to appear only in certain chunks.

    @return: A tuple. First element is a list of matched chunks. If
            keywords was specified, will only return chunks where a
            keyword was contained in it
            Second element is a list of matched keywords. Only use if
            keywords was specified
    '''

    # find all possible permutation of the regex
    expressions = list(itertools.permutations(exp, len(exp)))
    minLen = float('inf')
    minIndex = 0
    # find the regex so that the tree has the least number of subtrees in order to maximize matching
    for i, expression in enumerate(expressions):
        expr = ""
        for e in expression:
            expr = expr+e
            expr = expr+"\n"
        tree = parse(line, expr, custom_tags)
        if (len(tree) < minLen):
            minIndex = i
            minLen = len(tree)
    # construct the optimal regex
    expr = ""
    for e in expressions[minIndex]:
        expr = expr+e
        expr = expr+"\n"
    return match_regex_and_keywords(line, expr, custom_tags, keywords)


if __name__ == "__main__":
    line = input("Enter some text: ")
    print(parse(line))
    # with open("tests/not_questions.txt") as f:
    #     for line in f:
    #         print(is_question(line))
    #         #print(match_regex_and_keywords(line, ""))
