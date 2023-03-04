import pickle
import pathlib
from nltk import word_tokenize
from nltk.util import ngrams
import math
from tqdm import tqdm   # This module function formats a nice loading bar

# If a future user of this code were to want to use other smoothing functions
# they could need to access the size of the source text, and this is what this
# does.


def count_tokens(filename):
    with open(pathlib.Path.cwd().joinpath(filename), 'r') as f:
        text = f.read().replace('\n', '')
        return len(word_tokenize(text))

# This is taken directly from Karen Mazidi's textbook. This function takes in
# unigrams and bigrams of a source text, as well as the number of tokens and
# unique tokens in that source text. It also takes in a new text as an argument
# to be evaluated, different probabilities are calcualted using a variety of
# smoothing functions. The equations for this function, and the laplace
# smoothing function can be found in the accompanying summary


def compute_prob(text, unigram_dict, bigram_dict, N, V):
    # N is the number of tokens
    # V is the number of unique tokens, the vocabulary size

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    p_gt = 1
    p_laplace = 1
    p_log = 0  # sometimes used to prevent overflow
    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        n_gt = bigram_dict[bigram] if bigram in bigram_dict else 1/N
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        if d == 0:
            p_gt = p_gt * (1 / N)
        else:
            p_gt = p_gt * (n_gt / d)
        p_laplace = p_laplace * ((n + 1) / (d + V))
        p_log = p_log + math.log((n + 1) / (d + V))
    return (p_gt, p_laplace, p_log)

# The main function reads in pickled dictionaries containing unigrams and
# bigrams of different languages: English, French, and Italian. Then, it
# loops through a file containing random strings from any of those languages,
# and uses the language ngrams to calcualte the probability of each string
# being in a given language. It also concurrently records it's results and
# prints the final accuracy calculated via given correct data.


def main():
    with open('english_uni.pickle', 'rb') as handle:
        english_uni = pickle.load(handle)

    with open('french_uni.pickle', 'rb') as handle:
        french_uni = pickle.load(handle)

    with open('italian_uni.pickle', 'rb') as handle:
        italian_uni = pickle.load(handle)

    with open('english_bi.pickle', 'rb') as handle:
        english_bi = pickle.load(handle)

    with open('french_bi.pickle', 'rb') as handle:
        french_bi = pickle.load(handle)

    with open('italian_bi.pickle', 'rb') as handle:
        italian_bi = pickle.load(handle)

    correct_count = 0
    total = 0
    missed_lines = []

    with open('LangId.sol', 'r') as solution_file:
        with open('LangID.prediction', 'w') as output_file:
            with open('LangId.test', 'r') as input_file:
                for i, line in tqdm(enumerate(input_file), total=300):
                    line = line.strip()
                    N = count_tokens("LangId.train.English")
                    V = len(english_uni)
                    english_prob = compute_prob(
                        line, english_uni, english_bi, N, V)
                    N = count_tokens("LangId.train.French")
                    V = len(french_uni)
                    french_prob = compute_prob(
                        line, french_uni, french_bi, N, V)
                    N = count_tokens("LangId.train.Italian")
                    V = len(italian_uni)
                    italian_prob = compute_prob(
                        line, italian_uni, italian_bi, N, V)

                    laplace = [
                        ("English", english_prob[1]),
                        ("French", french_prob[1]),
                        ("Italian", italian_prob[1])]

                    max_value = max(laplace, key=lambda x: x[1])

                    answer = solution_file.readline().split()[1]
                    total = total + 1
                    if answer == max_value[0]:
                        correct_count = correct_count + 1
                    else:
                        missed_lines.append(i-1)

                    output_file.write(str(i-1) + ' ' + max_value[0] + '\n')

    print("Done!")
    print("Accuracy of %.2f. Missclassified items at lines: " %
          ((correct_count/total)*100))
    print(missed_lines)


main()
