import os
import re   #regex module
import nltk

import utils
#from util import utils

def parse(line, expression):
    '''
    Looks for a certain type of phrase for all the sentences in a file

    @param line: The sentence to check
    @param expression: A raw string containing the regular expression
            chunk to match. This is utilizing nltk's regex parser

    @return: The syntax tree representing the parsed sentence
    '''

    try:
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

    except Exception as e:
        print(str(e))

    return parsed_text

def is_question(line):
    '''
    Checks if a sentence is a question

    @param line: The sentence to check

    @return: Boolean saying whether the sentence is a question
    '''
    tree = parse(line, r"question: {<W..?>}")

    '''
    for subtree in tree.subtrees(
            filter=lambda tree: tree.label() == "question"):
        print(subtree)
    '''
    #checks if any question chunks were found
    return len(
            list(tree.subtrees(
                filter=lambda tree: tree.label() == "question"))) > 0

def search_for_location(line):
    """
    Verifies if passed in chunks are names of cities/locations

    Assumptions made:
    If the statement is about weather, then all named entities are treated
    as a location (this includes ORGANIZATION, PERSON tags)

    This function has been observed to fail on the case:
    "weather in San Francisco"

    @param line: the text to search through

    @return: a string of the found location, if none found, returns None
    """
    '''
    NER_TAGGER = nltk.StanfordNERTagger(
        "%s/dep/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz"%(os.getcwd()))
    '''
    loc_labels = ["GPE", "ORGANIZATION", "PERSON"]

    tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(line)))
    tree.draw()

    '''
    tags = NER_TAGGER.tag(line.split())
    print(tags)
    '''
    
    location = ""
    for subtree in tree.subtrees(lambda t: t.label() == "S"):
        for chunk in subtree.subtrees(lambda t: t.height() == 2):
            if isinstance(chunk, str):
                continue
            '''
            print("cur chunk: ") == type("")
            print(chunk)
            '''

            if chunk.label() in loc_labels:
                location_elem = ""
                for word, pos in chunk:
                    location_elem += word + " "
                #print("cur elem: ")
                #print(location_elem)
                location_elem = location_elem.strip()

                location += location_elem + ", "

    location = location.strip(" ,")
    if location != "":
        print("found location %s"%(location))
    else:
        print("No location found")
    return location

def match_regex_and_keywords(line, exp, keywords=None):
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
    tree = parse(line, exp)

    #only loop over full trees, not subtrees or leaves
    #only root node has the "S" label
    for subtree in tree.subtrees(lambda t: t.label() == "S"):

        #now loop through subtrees, detected chunks have height 2
        for chunk in subtree.subtrees(lambda t: t.height() == 2):
            if keywords == None:
                #no keyword detection needed
                matched_chunks.append(chunk)
            else:
                #the format is (<word>, <pos_tag>) for a single word
                for word, tag in chunk.leaves():
                    if word in keywords:
                        matched_chunks.append(chunk)
                        matched_keywords.append(word)
                        break

    return (matched_chunks, matched_keywords)

if __name__ == "__main__":
    with open("tests/not_questions.txt") as f:
        for line in f:
            print(is_question(line))
            #print(match_regex_and_keywords(line, ""))
