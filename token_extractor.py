import nltk
#nltk.download()
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.book import*
import string

def token_extract(text):
    tokens = word_tokenize(text)  # tokenize text
    unique_tokens = set(tokens)     # set unique tokens
    fdist = FreqDist(unique_tokens)  # get frequency distribution

    vocab = {}  #dictionary
    for token in unique_tokens:
        if token in vocab:
            vocab[token] += 1
        else:
            vocab[token] = 1
    print(vocab)
    print(fdist)
    return fdist, vocab

text = "i hate you hate"
token_extract(text)

'''
Need to add functionality to print top 25-40 terms.
'''


