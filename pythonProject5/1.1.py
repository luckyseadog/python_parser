from typing import List, Tuple, Optional
from urllib.request import urlopen
import re

from bs4 import BeautifulSoup

#https://habr.com/ru/post/543760/


from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.data = ''


    def handle_data(self, data):
        self.data += data





def download_html(link:str) -> str:
    response = urlopen(link)
    headers = response.headers
    data = response.read()
    data_decoded = data.decode('utf-8')

    return headers, data_decoded


response_headers, response = download_html('https://habr.com/ru/post/543760/')

data_response = response.strip().split()

parser = MyHTMLParser()
parser.feed(response)
raw_data = parser.data

token_pattern = re.compile(r'[\s][A-Za-zА-Яа-я][A-Za-zА-Яа-я]+[\s]')
#token_pattern = re.compile(r'\b[A-Za-zА-Яа-я][A-Za-zА-Яа-я]+\b')
raw_data = token_pattern.findall(raw_data)
raw_data = [i.strip() for i in raw_data]

data_for_user = []
dict_EN = []

with open('english_words.txt', 'r') as f:
    for word in f.readlines():
        if re.match(r'\w\w+', word):
            dict_EN.append(word.strip())

for word in raw_data:
    if not(re.match(r'[А-Яа-я]', word)):
        if word in dict_EN:
            data_for_user.append(word)
    elif re.match(r'[А-Яа-я]', word):
        data_for_user.append(word)

print(float(len(''.join(data_for_user)))/float(len(''.join(data_response))))

#print('Пропорция нужных данных: ', float(len(''.join(data_for_user)))/float(print(len(''.join(data_response)))))
