# CS4301.001 - Project
# Ricardo Alanis
# Thomas Dang
# Alan Stock
from bs4 import BeautifulSoup
from queue import Queue
import glob
import nltk
import os
import re
import requests
import urllib


REQUIRED_URLS = 10
START_URL = "http://www.nba.com/cavaliers/"
IGNORED_SITES = ['facebook', 'google', 'twitter', 'linkedin', 'video']


'''
Write a function to loop through your urls and and scrape all text off each page. 
Store each page’s text in its own file. 
'''


def scrape(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)

    soup = BeautifulSoup(con, "lxml")

    data = soup.findAll(text=True)
    result = filter(visible, data)

    temp_list = list(result)  # list from filter
    temp_str = ' '.join(temp_list).encode('utf-8')

    file_name = '{}.txt'.format(url.replace("/", "-")[-30:])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'raw')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass  # already exists
    path = os.path.join(dest_dir, file_name)
    with open(path, 'w') as output:
        output.write(str(temp_str))


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
    cleanfile = 'clean_{}'.format(rawfile[4:37])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'clean')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass  # already exists
    path = os.path.join(dest_dir, cleanfile)
    with open(rawfile) as f:
        with open(path, 'w') as output:
            text = f.read()

            mapping = [('\\n', ''), ('\\t', ''), ('\s+', ' ')]
            for k, v in mapping:
                text = text.replace(k, v, text)

            output.write(text)


'''
Write a function to extract at least 10 important terms from the pages using an importance measure 
such as term frequency. First, it’s a good idea to lower-case everything, remove stopwords and punctuation. 
Then build a vocabulary of unique terms. Create a dictionary of unique terms where the key is the token and 
the value is the count across all documents.  Print the top 25-40 terms.
'''
# stop_words = set(stopwords.words('english'))
# important_words = [w for w in set(tokens) if w not in stop_words]
# important_words.lower()
# Remove punct?
# FreqDist


         #   sentences = nltk.sent_tokenize(text)
         #   for s in sentences:
         #       for w in s:
         #           unidecode(w)
         #       output.write(s)

#  temp_str = temp_str.replace('\n', '')  # replace all newlines with space
#  temp_str = temp_str.lower()  # lowercase all letters
#  temp_str = re.sub(r'\d+', '', temp_str)  # remove all digits
#  temp_str = re.sub(r"\*+[,.\";'()\-@#?!&:$]+\*", " ", temp_str)  # remove punctuation


def extractTokens(text):
    tokens = nltk.word_tokenize(text)  # tokenize text
    unique_tokens = set(tokens)  # set unique tokens
    fdist = nltk.FreqDist(unique_tokens)  # get frequency distribution

    vocab = {}  # dictionary
    for token in unique_tokens:
        if token in vocab:
            vocab[token] += 1
        else:
            vocab[token] = 1

    return fdist, vocab


def main():
    q = Queue()
    q.put(START_URL)
    relevant_urls = set()
    visited_urls = set()

    while len(relevant_urls) < REQUIRED_URLS:
        url = q.get()
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html5lib")

        for link in soup.find_all('a'):
            link_str = str(link.get('href'))

            if link_str.startswith('http') and link_str not in visited_urls:
                q.put(link_str)
                visited_urls.add(link_str)

                if 'Lebron' in link_str or 'lebron' in link_str and link_str not in relevant_urls:
                    if not any(badurl in link_str for badurl in IGNORED_SITES):
                        relevant_urls.add(link_str)
                        print(link_str)
                        scrape(link_str)

    with open("urls.txt", "w") as output:
        output.write(str(relevant_urls))

    search_str = os.path.join('raw', '*.txt')
    files = glob.glob(search_str)
    for filename in files:
        cleanup(filename)

    # extractTokens()

if __name__ == "__main__":
    main()