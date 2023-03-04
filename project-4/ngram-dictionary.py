import pathlib
import pickle
from nltk import word_tokenize
from nltk.util import ngrams

# Creates dictionaries of unique ngrams and the counts of those ngrams from a
# given filename 
def gen_ngram(filename):
    with open(pathlib.Path.cwd().joinpath(filename), 'r') as f:
        text = f.read().replace('\n','')
    
    unigrams = word_tokenize(text)
    
    # How to make ngrams without nltk
    # bigrams = [(unigrams[k], unigrams[k + 1]) for k in range(len(unigrams)-1)]
    bigrams = list(ngrams(unigrams, 2))
    
    # Create dictionaries
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}
    
    
    return (unigram_dict, bigram_dict)

# This function creates bigram and unigram dictionaries for the given lagnauge
# files and pickles them
def main():
    english_uni, english_bi = gen_ngram("LangId.train.English")
    french_uni, french_bi = gen_ngram("LangId.train.French")
    italian_uni, italian_bi = gen_ngram("LangId.train.Italian")
    
    print("Hello")
    
    # Test successful count, it's a long runtime
    out = dict(list(english_uni.items())[0: 5])
    print(out)
    
    with open('english_uni.pickle', 'wb') as handle:
        pickle.dump(english_uni, handle)
        
    with open('french_uni.pickle', 'wb') as handle:
        pickle.dump(french_uni, handle)
        
    with open('italian_uni.pickle', 'wb') as handle:
        pickle.dump(italian_uni, handle)
        
    with open('english_bi.pickle', 'wb') as handle:
        pickle.dump(english_bi, handle)
        
    with open('french_bi.pickle', 'wb') as handle:
        pickle.dump(french_bi, handle)
        
    with open('italian_bi.pickle', 'wb') as handle:
        pickle.dump(italian_bi, handle)
        
main()