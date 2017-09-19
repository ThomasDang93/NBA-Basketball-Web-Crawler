# CS4301.001 - Project
# Ricardo Alanis
# Thomas Dang
# Alan Stock

from bs4 import BeautifulSoup
import requests


def main():
    starter_url = "http://nba.com"

    r = requests.get(starter_url)

    data = r.text
    soup = BeautifulSoup(data, "html5lib")

    # write urls to a file
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):
            print(link.get('href'))
            f.write(str(link.get('href')) + '\n\n')


if __name__ == "__main__":
    main()