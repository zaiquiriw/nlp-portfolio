import pickle

topTenWords = ['despicable', 'film', 'gru', 'minions', 'animation',
               'fan', 'illumination', 'universal', 'movie', 'animated']

knowledgeBase = {}

for word in topTenWords:
    sentencesContaining = []
    for i in range(30):
        filename = f"{i}textfileclean.txt"
        with open(filename, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
        lines = text.lower().split("\n")
        for line in lines:
            if word in line:
                sentencesContaining.append(line)
    knowledgeBase[word] = sentencesContaining

print(knowledgeBase['minions'][:100])
with open(f'kb.pickle', 'wb') as f:
    pickle.dump(knowledgeBase, f)
