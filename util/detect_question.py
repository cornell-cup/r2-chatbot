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

with open("../tests/not_questions.txt") as f:
    for line in f:
        print(is_question(line))

