from typing import List, Tuple, Optional
from urllib.request import urlopen
import re
from html.parser import HTMLParser

#https://habr.com/ru/post/543760/

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.depth = 0
        self.best_depth = 1000
        self.best_data = ''
        self.html_data = ''

    def handle_starttag(self, tag, attrs):
        self.depth += 1
        self.html_data = del_space(self.get_starttag_text())

    def handle_data(self, data):
        ''' There we find data which is the least deep
         and consists of text on morw than 80% '''
        self.html_data += del_space(data)
        changed_data = re.findall(r'[А-Яа-я]+', del_space(data))
        changed_data = ''.join(changed_data)
        if self.html_data:
            if len(changed_data)/len(self.html_data) > 0.8:
                if self.best_depth > self.depth:
                    self.best_data = data
                    self.best_depth = self.depth

    def handle_endtag(self, tag):
        self.depth -= 1


def del_space(data:str) -> str:
    '''Removing spaces'''
    return ''.join([i for i in data if i != ' '])

def download_html(link:str) -> str:
    '''Getting decoded data'''
    response = urlopen(link)
    headers = response.headers
    data = response.read()
    data_decoded = data.decode('utf-8')

    return headers, data_decoded




response_headers, response = download_html('https://habr.com/ru/post/543760/')
print(response)

parser = MyHTMLParser()
parser.feed(response)
print('_________________________________')
print(parser.best_data)
print(parser.best_depth)
