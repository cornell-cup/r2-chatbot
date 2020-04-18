import re   #regex module
import nltk

import utils

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
        parsed_text.draw()
            
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

def search_for_location(chunks):
    """
    Verifies if passed in chunks are names of cities/locations

    Assumptions made:
    If the statement is about weather, then all named entities are treated
    as a location (this includes ORGANIZATION, PERSON tags)

    @param chunks: a list of nltk chunks

    @return: a list of strings containing found locations
    """
    print("all chunks: ")
    print(chunks)
    for chunk in chunks:
        if isinstance(chunk, str):
            continue
        line = ""
        print("cur chunk: ") == type("")
        print(chunk)
        for word, tag in chunk.leaves():
            line += word + " "
        print("line from chunk: " + line)
        
        cap = utils.capitalize_all(line)
        
        #nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize()))
        tokenized_line = nltk.word_tokenize(cap)
        pos_tagged = nltk.pos_tag(tokenized_line)

        thing = nltk.ne_chunk(pos_tagged)
        thing.draw()
        for t in thing.subtrees():
            if t.label() == 'GPE':
                print(t)

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
            print("nlp_util chunk: ")
            print(chunk)
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

