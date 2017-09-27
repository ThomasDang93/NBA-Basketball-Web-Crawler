import os
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
#from nltk.book import*
import string
from bs4 import BeautifulSoup
import urllib.request
import re
from nltk.tokenize import sent_tokenize
from bs4.element import Comment
import urllib

#fdist_cumulative = FreqDist()
my_url = "https://www.usatoday.com/story/sports/nba/2017/09/25/lebron-james-donald-trump-the-people-run-country-not-one-individual/700682001/"

# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'meta']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

html = urllib.request.urlopen(my_url)
soup = BeautifulSoup(html,"lxml")
data = soup.findAll(text=True)
result = filter(visible, data)
temp_list = list(result)      # list from filter
temp_str = ' '.join(temp_list)

temp_str = temp_str.replace('\n','')            #replace all newlines with space
temp_str = temp_str.lower()                     #lowercase all letters
temp_str = re.sub(r'\d+', '', temp_str)         #remove all digits
temp_str = re.sub(r"\*+[,.\";'()\-@#?!&:$]+\*", " ", temp_str)     #remove punctuation
tokens = word_tokenize(temp_str)                #tokenize words
tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]     #remove stopwords and punctuations
#fdist = FreqDist(tokens)                #get frequency distribution
#fdist_cumulative += fdist

print(temp_str)
print(tokens)
#print(fdist)

sents = sent_tokenize(temp_str)
for sent in sents:
    print(sent)
