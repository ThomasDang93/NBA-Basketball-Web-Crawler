# CS4301.001 - Project
# Ricardo Alanis
# Thomas Dang
# Alan Stock

import glob
import operator
import nltk
import os
import re
import requests
import string
import urllib

from bs4 import BeautifulSoup
from collections import Counter
from queue import Queue
from nltk.corpus import stopwords

REQUIRED_URLS = 15
START_URL = "http://www.nba.com/cavaliers/"
IGNORED_URL_STRINGS = ['facebook', 'google', 'twitter', 'linkedin', 'video', 'insider/story', 'wade']
TOP_TERMS_PER_PAGE = 10
TOP_TERMS_IN_DICT = 40

'''
Write a function to loop through your urls and and scrape all text off each page. 
Store each page’s text in its own file. 
'''


def scrape(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)
    page = con.read().decode('utf-8')

    soup = BeautifulSoup(page, "lxml")
    data = soup.findAll(text=True)
    result = filter(visible, data)
    scrape_str = ' '.join(list(result)).encode('ascii', 'replace')

    file_name = '{}.txt'.format(url.replace("/", "-")[-30:])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'raw')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass  # already exists
    path = os.path.join(dest_dir, file_name)
    with open(path, 'w') as output:
        output.write(str(scrape_str))


'''
function to determine if an element is visible
'''


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'meta']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


'''
Write a function to clean up the text. You might need to delete newlines and tabs. 
Extract sentences with NLTK’s sentence tokenizer. Write the sentences for each file to a new file. 
That is, if you have 15 files in, you have 15 files out. 
You might need to clean up the cleaned up files manually to delete irrelevant material. 
'''


def cleanup(rawfile):
    cleanfile = 'clean_{}'.format(rawfile[4:38])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'clean')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass
    path = os.path.join(dest_dir, cleanfile)
    with open(rawfile) as f:
        with open(path, 'w') as output:
            text = f.read()

            mapping = [('\\n', ''), ('\\t', ''), ('\\s\\s+', ' '), ("\\'","'")]
            for k, v in mapping:
                text = text.replace(k, v)
            sentences = nltk.sent_tokenize(text)
            for s in sentences:
                output.write(s)


'''
Write a function to extract at least 10 important terms from the pages using an importance measure 
such as term frequency. First, it’s a good idea to lower-case everything, remove stopwords and punctuation. 
Then build a vocabulary of unique terms. Create a dictionary of unique terms where the key is the token and 
the value is the count across all documents.  Print the top 25-40 terms.
'''


def extract_terms(text):
    translate_table = dict((ord(char), None) for char in string.punctuation)
    text = text.translate(translate_table)
    tokens = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    fdist = nltk.FreqDist(tokens)

    return set(fdist.most_common(TOP_TERMS_PER_PAGE))

    # for term in fdist.most_common(TOP_TERMS_PER_PAGE):
    #    if term in top_terms:
    #        top_terms[term] += 1
    #    else:
    #        top_terms[term] = 1

    # return top_terms


def main():
    q = Queue()
    relevant_urls = set()
    found__urls = set()

    q.put(START_URL)
    while len(relevant_urls) < REQUIRED_URLS:
        url = q.get()
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html5lib")

        for link in soup.find_all('a'):
            link_str = str(link.get('href'))

            if link_str.startswith('http') and link_str not in found__urls:
                q.put(link_str)
                found__urls.add(link_str)

                if ('lebron' in link_str and
                        link_str not in relevant_urls and
                        not any(url_str in link_str for url_str in IGNORED_URL_STRINGS)
                    ):
                        relevant_urls.add(link_str)
                        print(link_str)
                        scrape(link_str)

    with open("urls.txt", "w") as output:
        output.write(str(relevant_urls))

    search_str = os.path.join('raw', '*.txt')
    files = glob.glob(search_str)
    for filename in files:
        cleanup(filename)

    vocab = Counter({})
    search_str = os.path.join('clean', '*.txt')
    files = glob.glob(search_str)
    for filename in files:
        with open(filename, 'r') as f:
            text = f.read()
            top_terms = extract_terms(text)
            page = Counter(dict(top_terms))
            vocab = vocab + page

    print(sorted(vocab, key=vocab.get, reverse=True)[:TOP_TERMS_IN_DICT])

if __name__ == "__main__":
    main()