# CS4301.001 - Project
# Ricardo Alanis
# Thomas Dang
# Alan Stock
import nltk
from bs4 import BeautifulSoup
from queue import Queue
import glob
import os
import requests


def main():
    url = "http://www.nba.com/cavaliers/"
    q = Queue()
    q.put(url)
    relevant_urls = set()
    scraped_urls = set()

    while len(relevant_urls) < 25:
        url = q.get()
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html5lib")

        for link in soup.find_all('a'):
            link_str = str(link.get('href'))

            if link_str.startswith('http') and link_str not in scraped_urls:
                q.put(link_str)
                scraped_urls.add(link_str)

                if 'Lebron' in link_str or 'lebron' in link_str and link_str not in relevant_urls:
                    relevant_urls.add(link_str)
                    scrape(link_str)

    with open("urls.txt", "w") as output:
        output.write(str(relevant_urls))

    search_str = os.path.join('raw', '*.txt')
    files = glob.glob(search_str)
    for filename in files:
        cleanup(filename)


'''
Write a function to loop through your urls and and scrape all text off each page. 
Store each page’s text in its own file. 
'''


def scrape(url):
    # beautifulsoup code here?
    text = "STUFF CAN BE IN Sentence of other phrases. This is an example. <img src = 'pict.jpg'>"

    file_name = '{}.txt'.format(url.replace("/", "-")[-25:])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'raw')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass  # already exists
    path = os.path.join(dest_dir, file_name)
    with open(path, 'w') as output:
        output.write(str(text))


'''
Write a function to clean up the text. You might need to delete newlines and tabs. 
Extract sentences with NLTK’s sentence tokenizer. Write the sentences for each file to a new file. 
That is, if you have 15 files in, you have 15 files out. 
You might need to clean up the cleaned up files manually to delete irrelevant material. 
'''


def cleanup(rawfile):
    cleanfile = 'clean_{}'.format(rawfile[4:32])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'clean')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass  # already exists
    path = os.path.join(dest_dir, cleanfile)
    with open(rawfile) as f:
        with open(path, 'w') as output:
            for line in f:
                tokens = nltk.word_tokenize(line)
                output.write(str(tokens).lower())


'''
Write a function to extract at least 10 important terms from the pages using an importance measure 
such as term frequency. First, it’s a good idea to lower-case everything, remove stopwords and punctuation. 
Then build a vocabulary of unique terms. Create a dictionary of unique terms where the key is the token and 
the value is the count across all documents.  Print the top 25-40 terms.
'''


if __name__ == "__main__":
    main()