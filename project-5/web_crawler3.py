import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def preprocessor(text):
    #tokenizes the text
    tokenList = word_tokenize(text.lower())

    #replaces the list with only alpha, not in stopwords
    tokenList = [token for token in tokenList if token.isalpha() and token not in stopwords.words('english')]

    # return tokens and nouns
    return tokenList

fullTokenList = []
for i in range(30):
    filename = f"{i}textfileclean.txt"
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    fullTokenList.extend(preprocessor(text))
freqDistWords = FreqDist(fullTokenList)
mostCommonWords = freqDistWords.most_common(25)
print(f'Top 25 most common words and their counts: {mostCommonWords}')