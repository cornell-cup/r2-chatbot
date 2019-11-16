import re   #regex module
import nltk

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
    return len(
            list(tree.subtrees(
                filter=lambda tree: tree.label() == "question"))) > 0

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

    @return: A list of matched chunks. If keywords was specified, will
            only return chunks where a keyword was contained in it
    '''
    tree = parse(line, exp)

if __name__ == "__main__":
    with open("../tests/not_questions.txt") as f:
        for line in f:
            print(is_question(line))

