import re   #regex module
import nltk

def parse(line, expression):
    '''
    Looks for a certain type of phrase for all the sentences in a file
    
    @param line: The sentence to check
    @param expression: A raw string containing the regular expression
            chunk to match. This is utilizing nltk's regex parser
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
        
        print(parsed_text)
        #parsed_text.draw()
            
    except Exception as e:
        print(str(e))

def is_question(line):
    '''
    Checks if a sentence is a question

    @param line: The sentence to check

    @return: Boolean saying whether the sentence is a question
    '''
    parse(line, r"question: {<W..?>}")

with open("keyword_tests.txt") as f:
    for line in f:
        is_question(line)

