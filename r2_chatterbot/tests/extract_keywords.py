from rake_nltk import Rake

# Uses stopwords for english from NLTK, and all puntuation characters by
# default
r = Rake()

# Extraction given the text.
#r.extract_keywords_from_text("keyword_tests.txt")

x = []
with open("question_keyword_tests.txt") as f:
    for line in f:
        x.append (line)
        r.extract_keywords_from_text(line)
        #print(r.get_ranked_phrases_with_scores())
        print(r.get_ranked_phrases())


# Extraction given the list of strings where each string is a sentence.
r.extract_keywords_from_sentences(x)

# To get keyword phrases ranked highest to lowest.
phrases = r.get_ranked_phrases()

# To get keyword phrases ranked highest to lowest with scores.
phrases_with_text = r.get_ranked_phrases_with_scores()

# print(phrases)
# print(phrases_with_text)
