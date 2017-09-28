from collections import Counter
import nltk
import string
from nltk.corpus import stopwords
TOP_TERMS_LIMIT = 6
def main():
    vocab_sum = Counter({})
    #fdist_sum = Counter(nltk.FreqDist())

    text = "i hate you hate why are mistakes! you hate my lebron mistakes wade is to me my carry lover of dine"
    text2nd = "can you see my mistakes he so i can lebron need you to be a there very careful. lebron? dine"

    vocab = extract_tokens(text)
    #fdist_sum += Counter(fdist)
    vocab_sum += Counter(vocab)

    vocab = extract_tokens(text2nd)
    #fdist_sum += Counter(fdist)
    vocab_sum += Counter(vocab)


    #print(fdist_sum)
    #print('\n')
    print("Merged dictionary using Counter:")
    print(vocab_sum)
    print('\n')
    print("Top 6 terms from the merged dictionary:")
    print(vocab_sum.most_common(TOP_TERMS_LIMIT))




def extract_tokens(text):

    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    #fdist = nltk.FreqDist(tokens)

    vocab = {}  # dictionary
    for token in tokens:
        if token in vocab:
            vocab[token] += 1
        else:
            vocab[token] = 1
    print("Vocabulary of text without stopwords and punctuation:")
    print(vocab)
    print('\n')
    #f = fdist.most_common(TOP_TERMS_LIMIT)

    return vocab

if __name__ == "__main__":
    main()



