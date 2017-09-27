# CS4301.001 - Project
# Ricardo Alanis
# Thomas Dang
# Alan Stock

from bs4 import BeautifulSoup
from queue import Queue
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

            if (link_str.startswith('http') and link_str not in scraped_urls):
                q.put(link_str)
                scraped_urls.add(link_str)

                if 'Lebron' in link_str or 'lebron' in link_str and link_str not in relevant_urls:
                    relevant_urls.add(link_str)
                    scrape(link_str)

    with open("urls.txt", "w") as output:
        output.write(str(relevant_urls))


'''
Write a function to loop through your urls and and scrape all text off each page. 
Store each page’s text in its own file. 
'''
def scrape(url):
    #beautifulsoup code here?
    text = "stuff"

    with open("{}.txt".format(url.replace("/","-")[-25:]), "w") as output:
        output.write(str(text))


'''
Write a function to clean up the text. You might need to delete newlines and tabs. 
Extract sentences with NLTK’s sentence tokenizer. Write the sentences for each file to a new file. 
That is, if you have 15 files in, you have 15 files out. 
You might need to clean up the cleaned up files manually to delete irrelevant material. 
'''


'''
Write a function to extract at least 10 important terms from the pages using an importance measure 
such as term frequency. First, it’s a good idea to lower-case everything, remove stopwords and punctuation. 
Then build a vocabulary of unique terms. Create a dictionary of unique terms where the key is the token and 
the value is the count across all documents.  Print the top 25-40 terms.
'''

if __name__ == "__main__":
    main()