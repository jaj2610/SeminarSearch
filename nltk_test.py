from bs4 import BeautifulSoup

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
f = open('test.html')
soup = BeautifulSoup(f.read().encode('utf-8'))
for tag in soup.find_all(text=lambda x: True):
    print pos_tag(word_tokenize(tag))