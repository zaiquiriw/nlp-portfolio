import os
import pandas as pd
import csv
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.chunk import ne_chunk
import string

# Set the directory path
dir_path = os.getcwd()

# Open a CSV file to write the data
with open('entity_data.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Question', 'Context'])

    # Loop through each file in the directory
    for filename in os.listdir(dir_path):
        # Check if the file is a text file and ends with 'clean.txt'
        if filename.endswith('clean.txt'):
            # Read in the file contents
            with open(os.path.join(dir_path, filename), 'r', encoding='utf8') as file:
                text = file.read()

            # Tokenize the text into sentences
            sentences = sent_tokenize(text)

            # Loop through each sentence and extract entities
            for sentence in sentences:
                words = word_tokenize(sentence)
                tagged = nltk.pos_tag(words)
                entities = ne_chunk(tagged)

                # Filter out the punctuation and non-unicode characters
                filtered_words = []
                for word in words:
                    # Filter out punctuation
                    filtered_word = ''.join(
                        c for c in word if c not in string.punctuation)
                    # Filter out non-unicode characters
                    if all(ord(c) < 128 for c in filtered_word):
                        filtered_words.append(filtered_word)

                # Join the remaining words back into a string
                clean_text = ' '.join(filtered_words)

                for entity in entities:
                    if hasattr(entity, 'label') and entity.label() in ['PERSON', 'ORGANIZATION', 'GPE']:
                        entity_text = ' '.join(c[0] for c in entity.leaves())
                        # quote = '"' + sentence + '"'
                        # question = '"' + entity_text + '"'
                        writer.writerow([entity_text, clean_text])
