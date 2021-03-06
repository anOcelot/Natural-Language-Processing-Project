import nltk
import ssl
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from bs4 import BeautifulSoup
import re


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
nltk.download('wordnet')
class TextAnalyzer:
  SENTENCE_SPLIT_REGEX = r'[.!?]+'

  WORD_OVER_SENTENCE_CONSTANT = 1.015
  SYLLABLE_OVER_WORD_CONSTANT = 84.6
  TOTAL_CONSTANT = 206.835

  def __init__(self, text):
    self.initialText = text
    self.tokens = text.split()
    self.syllableDictionary = {}

  def fullPass(self):
    self.calculate()
    self.display()
    self.upgrade()

  def calculate(self):
    self.sentenceCount = len(re.split(self.SENTENCE_SPLIT_REGEX, self.initialText))
    self.syllableCount = self.__countAllSyllables(self.tokens)
    self.wordCount = len(self.tokens)

    # Sentence Length Ratio
    part1 = self.WORD_OVER_SENTENCE_CONSTANT * (self.wordCount / self.sentenceCount)

    # Word Length Ratio
    part2 = self.SYLLABLE_OVER_WORD_CONSTANT * (self.syllableCount / self.wordCount)

    self.score = self.TOTAL_CONSTANT - part1 - part2

  def display(self):
    print("Sentence Count:\t" + str(self.sentenceCount))
    print("Word Count:\t" + str(self.wordCount))
    print("Syllable Count:\t" + str(self.syllableCount))

    print("Score:\t\t" + str(self.score))
    print("Classification:\t" + self.__classifyText())


  def countSyllablesInWord(word):
    return len(''.join(c if c in "aeiouy"else' ' for c in word.rstrip('e')).split())

  @staticmethod
  def upgrade_word(word):
    maxSyllables = countSyllablesInWord(word)
    bestCandidate = word
    tagged = nltk.pos_tag({word})[0]
    #print ("Word to upgrade:" + word)
    
    #make sure there are actually synonym sets
    if len(wn.synsets(word)) > 0:
      
      #iterate across synonyms and return the word with the most synonyms
      #iterating across the 1st synset since it will tend to contain words closer in meaning
      for synonym in wn.synsets(word)[0].lemma_names():
        #tag the possible replacement w/ its part of speech
        taggedPossible = nltk.pos_tag({synonym})[0]
        
        #if the potential replacement has more syllables, and is the exact same part of speech, 
        #it becomes the best candidate
        if (countSyllablesInWord(synonym) > maxSyllables) and tagged[1] == taggedPossible[1]:
          bestCandidate = synonym

    return bestCandidate




  def upgrade(self):

    # 1. Determine what words NOT to change (aka proper nouns, numbers in them, certian phrases aka gold medal?)
    # 2. How many of the left over words to "upgrade" -- to what degree? (college, or just 7th grade?)
    # 3. Find similar words for each of the words to upgrade, making sure the new word has more syllables
    # 4. Profit

    #just counting these for debugging purposes
    nouns = 0
    verbs = 0
    articles = 0

    #tag the tokenzid version of the text w/ the POS of each word
    tagged = nltk.pos_tag(self.tokens)

    #for now, replace only basic nouns and verbs
    for word in tagged:
      if 'NN' in word[1]:
        nouns += 1
        #replace all instances of the word in the text
        self.initialText = self.initialText.replace(word[0], self.upgrade_word(word[0]))

      elif 'VB' in word[1]:
        verbs += 1
        self.initialText = self.initialText.replace(word[0], self.upgrade_word(word[0]))

    #print (self.initialText)





  def __countAllSyllables(self, tokens):
    return sum([ val for val in [self.__countSyllablesInWord(word) for word in tokens] if val is not None])

  # https://codegolf.stackexchange.com/a/47326
  def __countSyllablesInWord(self, word):
    return len(''.join(c if c in"aeiouy"else' 'for c in word.rstrip('e')).split())

  def __classifyText(self):
    if self.score is None:
      return None
    elif self.score >= 90:
      return "5th Grade"
    elif self.score >= 80 and self.score < 90:
      return "6th Grade"
    elif self.score >=70 and self.score < 80:
      return "7th Grade"
    elif self.score >=60 and self.score < 70:
      return "8th & 9th Grade"
    elif self.score >=50 and self.score < 60:
      return "10th to 12th Grade"
    elif self.score >=30 and self.score < 50:
      return "College"
    else:
      return "College Graduate"


def countSyllablesInWord(word):
  return len(''.join(c if c in "aeiouy"else' ' for c in word.rstrip('e')).split())
