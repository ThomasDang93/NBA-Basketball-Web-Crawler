# CS4301.001 - Project
# Ricardo Alanis
# Thomas Dang
# Alan Stock

from bs4 import BeautifulSoup
from queue import Queue
import requests


def main():

    q = Queue()
    q.put("http://www.nba.com/cavaliers/")
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

            if 'Lebron' in link_str or 'lebron' in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if link_str.startswith('http') and 'google' not in link_str:
                    if link_str not in relevant_urls:
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


if __name__ == "__main__":
    main()