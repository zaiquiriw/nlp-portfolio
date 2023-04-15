import nltk
import re

for i in range(30):
    filename = f"{i}textfile.txt"
    newFilename = f"{i}textfileclean.txt"
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    text_chunks = [chunk for chunk in text.splitlines() if not re.match(r'^\s*$', chunk)]
    cleanText = ""
    for i, chunk in enumerate(text_chunks):
        cleanText += chunk.strip()
        cleanText += '\n'
    sentences = nltk.sent_tokenize(cleanText)
    with open(newFilename, 'w', encoding='utf-8') as f1:
        for sentence in sentences:
            f1.write(sentence)
            f1.write("\n")