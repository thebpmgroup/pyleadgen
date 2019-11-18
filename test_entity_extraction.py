#import nltk
import spacy
from pprint import pprint
from collections import Counter

nlp = spacy.load("en_core_web_sm")

'''
def preprocessing(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

nltk.app.chunkparser()
'''
f=open("pagetext", "r")
text = f.read()

doc = nlp(text)
labels = [x.label_ for x in doc.ents]
print(Counter(labels))
print(Counter(labels).most_common(3))

items = [x.text for x in doc.ents]
print(Counter(items).most_common(5))
#pprint([(X.text, X.label_) for X in doc.ents])
'''
sentences = preprocessing(text)
for sentence in sentences:
    print(sentence)
'''