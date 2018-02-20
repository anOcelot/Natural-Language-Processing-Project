import nltk
from text_analyzer import TextAnalyzer
from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')
from nltk.corpus import wordnet as wn


with open('text/Beowulf2.txt', 'r') as textFile:
    data=textFile.read().replace('\n', '')

#with open('text/meditations.txt', 'r') as textFile:
# data=textFile.read().replace('\n', '')

def countSyllablesInWord(word):
    return len(''.join(c if c in "aeiouy"else' ' for c in word.rstrip('e')).split())


def upgradeWord(word):
    all = [item for sublist in [sim.lemma_names() for sim in wn.synsets(word)] for item in sublist]
    winner = None
    val = 0

    for w in all:
        c = countSyllablesInWord(w)
        if c > val:
            winner = w
            val = c
   #print (all)
    return winner

def upgradeWordV2(word):
    max = 0
    maxword = ""
    for word in wn.synsets(word)[0].lemma_names():
        if countSyllablesInWord(word) > max:
            #print(word)
            maxword = word

    return maxword


# with open('text/7th-grade/article-1.txt', 'r') as textFile:
#     data = textFile.read().replace('\n', '')

#splitWords = data.split()
#wordLength = len(splitWords)

#rangeCount = 10
#rangeAmount = wordLength // rangeCount

# for x in range(0, rangeCount):
#     start = x * rangeAmount
#     end = start + rangeAmount
#
#     txt = ' '.join(splitWords[start:end])
#     print("Words: " + str(start) + " - " + str(end))
#     datas[x] = TextAnalyzer(txt).fullPass()
#     print("\n\n")

# splitData = " ".join(data.split()[1000:2000])

TextAnalyzer(data).fullPass()
# TextAnalyzer(splitData).fullPass()
import pdb;

#pdb.set_trace()
#print (wn.synsets("bird")[0].lemma_names())
#print (wn.synsets("cat")[0].definition())
#print (TextAnalyzer.upgrade_word("cat"))
test = TextAnalyzer("reading book in winter in the state of michigan")

#hit = wn.synsets("hit")[0]
# cat = wn.synsets("cat")[0]
# one = []
# two = []
# for synset in wn.synsets("cat"):
#     print (synset.lch_similarity(cat))
#     two.append(synset.path_similarity(cat))
#     #print (synset.lemma_names())
#     #print (synset.definition())
#     #print ('\n')
#print (one)
#print (two)

#test.upgrade()
#print (test.upgrade_word("did"))
