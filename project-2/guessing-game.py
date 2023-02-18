import sys		# For parsing data
import pathlib  # For parsing data
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

# This simply reads the filename


def parseText(filename):
    with open(pathlib.Path.cwd().joinpath(filename), 'r') as f:
        text_in = f.read()
    return text_in

# createDictionary evaluates which nouns are used the most, and returns a list
# containing a numCommon number of the most used nouns in the nouns list.


def createDictionary(tokens, nouns, numCommon):
    count = {}
    dictionary = []

    # Create a dictionary to store the count for each noun
    for words in nouns:
        count[words] = tokens.count(words)

    # Sort the dictionary and take the appropriate number of nouns to return
    print("Most common " + str(numCommon) + " words are: ")
    for word in sorted(count, key=count.get, reverse=True)[:numCommon]:
        print(word, ":", count[word])
        dictionary.append(word)

    return dictionary

# This parses the 'blank' dictionary, in which the key is a letter of the word
# being guessed, and the value is whether the player has guessed it. It then
# prints a string, containing either the letters of the word, or blanks if the
# player has yet to guess


def printBlank(blank, word):
    formattedBlank = ''
    for letter in word:
        if blank[letter]:
            formattedBlank = formattedBlank + '_'
        else:
            formattedBlank = formattedBlank + letter
    return formattedBlank

# This game takes a dictionary of words, picks a random word from that list and
# takes input prompts from the player to see if they can guess the word letter
# by letter. The game scores you on how many times you miss, keeps track of
# score and progress, and is exitable via the '!' key. If the player has won,
# the game may continue because again is set to true.


def guessingGame(dictionary, score):
    again = False
    # score = 5, the starting default score (Could have been a parameter)
    word = dictionary[randint(0, len(dictionary)-1)]  # Getting the random word

    # Blank serves as a dictionary to keep track of which letters are still
    # blank. If the player guesses a character in the word, it is in blank and
    # the value of blank for that letter is set to false. This lets us check
    # if a guess is correct in O(1) time
    blank = {}
    for letter in word:
        blank[letter] = True

    # Inorder to check if the game is won, I keep track of how many correct
    # guesses there have been so we don't have to check string equality (O(N))
    # every guess, instead we can just compare ints (O(1))
    uniqueLetters = len(blank)
    correctGuesses = 0

    # We parse the 'blank' dictionary to create blank word
    newBlank = printBlank(blank, word)
    print("Welcome to my guessing game, you have " +
          str(score) + " attempts... for now")
    print("Your word is, " + newBlank + "!")
    print("Guess ! to quit at any time.")
    while True:
        # Every guess, we simply set the player not be correct, but if they
        # successfully make a match then we set correct to true!
        correct = False
        letter = input("What do you choose? ")[0:]
        if letter == '!':
            print("You'll get 'em next time!")
            break
        # "If the guessed letter is in the blank dictionary, and you have not
        # already guessed it, then a correct guess has been made!"
        if letter in blank and blank[letter] == True:
            blank[letter] = False
            correct = True
            correctGuesses = correctGuesses + 1

        # If no correct guess was made the player still has correct = false
        # And now we can parse a new blank line with the letters filled in
        newBlank = printBlank(blank, word)

        # Response if guess was wrong
        if not correct:
            score = score - 1
            # If the player has lost (score < 0), end the game
            if score < 0:
                print("Looks like the word " + word +
                      " was too hard! Try again next time!")
                break
            print("Sorry guess again. Your score is " + str(score) +
                  " and your word is still " + newBlank + ".")

        # Response if guess was correct
        else:
            score = score + 1
            print("Right! Your word is: " + newBlank +
                  " and your score is: " + str(score) + ".")
            # If the player has made the correct number of guesses, hooray!
            if correctGuesses == uniqueLetters:
                print("Nice job! Good job guessing the word was " + word +
                      ". You won with " + str(score) + " too!")
                again = True
                break

    if again == True:
        print("Guess another word, you got this!")
        guessingGame(dictionary, score)

    return


def preprocess(text):
    # The assignment asks us to read lexical diversity before the preprocessing
    # step, but for consistency I am going to preform it after the tokenization
    tokens = word_tokenize(text)

    # I'm going to assume the input isn't lowercase and add this in
    tokens = [t.lower() for t in tokens]
    numTokens = len(tokens)

    # The number of unique tokens out of the set of all tokens
    uniqueTokens = set(tokens)
    print("Lexical Diversity: %.2f" % (len(uniqueTokens) / numTokens))

    # I didn't know how python global scope worked! Variables are loaded global
    # to the scope of the module. To modify a variable with global scope, we
    # must define it as such.
    # Reduce the tokens to alphas, those not in the stopword list, and have a
    # length geater than 5. (Using list comprehension)
    global stopwords
    stopwords = stopwords.words('english')
    tokens = [t for t in tokens if t.isalpha() and len(t) >
              5 and t not in stopwords]
    print(tokens[:20])

    # Now we have our tokens defined we lemmatize them and tag parts of speech
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in tokens]
    uniqueLemmas = set(lemmatized)
    taggedLemmas = nltk.pos_tag(uniqueLemmas)

    # Print the first 20 tagged, and make a list of nouns
    print("Listing the first 20 POS Tagged:")
    for token, pos in taggedLemmas[:20]:
        print(token + " --> " + pos)
    nouns = [t[0] for t in taggedLemmas if t[1] == "NN"]

    # Print the number of tokens and nouns
    print("There are " + str(numTokens) + " tokens, and only " +
          str(len(nouns)) + " nouns.")

    # Return the number of tokens and nouns
    return (tokens, nouns)


# Parses system arguments, and runs the various functions
def main():
    if len(sys.argv) < 2:
        print('Please enter a filename as a system argument')
    else:
        filename = sys.argv[1]
        corpus = parseText(filename)
        tokens, nouns = preprocess(corpus)
        dictionary = createDictionary(tokens, nouns, 50)
        seed(1234)  # Random seed for the num generator for reproducability
        guessingGame(dictionary, 5)
    return


if __name__ == '__main__':
    main()
