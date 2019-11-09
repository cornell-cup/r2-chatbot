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

