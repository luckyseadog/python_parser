from typing import List, Tuple, Optional
from urllib.request import urlopen
import re
from html.parser import HTMLParser


#https://www.msveta.ru/catalog/bra-dvoynye/
#https://www.pizzahot.me/cat/picca/


class MyHTMLParser(HTMLParser):
    '''Parser for getting paths with frequencies over two types of data
    price and name of product'''

    def __init__(self):
        super().__init__()
        self.current_path = []
        self.needed_paths = {}

    def handle_data(self, data):
        if re.fullmatch(r'\d+\s+руб\.\s+', data):
            # print('data price: ', data)
            path = ' '.join(self.current_path)
            if path in self.needed_paths:
                self.needed_paths[path] += 1
            else:
                self.needed_paths[path] = 1


        if re.fullmatch(r'\d?\d?[А-Яа-я]*\s?[А-Яа-я]+\s?\d?\.?\d?[&]?\s?[А-Яа-я]*', data):
            path = ' '.join(self.current_path)
            if path in self.needed_paths:
                self.needed_paths[path] += 1
            else:
                self.needed_paths[path] = 1

    def handle_starttag(self, tag, attrs):
        self.current_path.append(tag)

    def handle_endtag(self, tag):
        ind = len(self.current_path) - self.current_path[::-1].index(tag) - 1
        self.current_path = self.current_path[:ind]


class ForTableHTMLParser(HTMLParser):
    '''Parser for getting data from the most common paths'''

    def __init__(self, true_path):
        super().__init__()
        self.current_path = []
        self.true_path = true_path
        self.data = []

    def handle_data(self, data):
        if self.current_path == self.true_path:
            self.data.append(data)

    def handle_starttag(self, tag, attrs):
        self.current_path.append(tag)

    def handle_endtag(self, tag):
        ind = len(self.current_path) - self.current_path[::-1].index(tag) - 1
        self.current_path = self.current_path[:ind]


class ForDictHTMLParser(HTMLParser):
    '''Parser for creating final dictionary'''

    def __init__(self, true_paths):
        super().__init__()
        self.current_path = []
        self.true_paths = true_paths
        self.main_dict = {}
        self.flag = False

    def handle_data(self, data):
        if self.current_path == self.true_paths[0]:
            self.type_product = data
            if not self.main_dict:
                self.main_dict = {data:{}}
            else:
                self.main_dict[data] = {}

        elif self.current_path == self.true_paths[1]:
            if self.flag == False:
                self.to_append = [None, None]
                self.to_append[0] = data
                self.flag = True
            else:
                self.to_append[1] = data
                self.main_dict[self.type_product][self.to_append[0]] = ' '.join([i for i in self.to_append[1].split()])
                self.flag = False

    def handle_starttag(self, tag, attrs):
        self.current_path.append(tag)

    def handle_endtag(self, tag):
        ind = len(self.current_path) - self.current_path[::-1].index(tag) - 1
        self.current_path = self.current_path[:ind]



def download_html(link:str) -> str:
    response = urlopen(link)
    headers = response.headers
    data = response.read()
    data_decoded = data.decode('utf-8')

    return headers, data_decoded


response_headers, response = download_html('https://www.pizzahot.me/cat/picca')


parser1 = MyHTMLParser()
parser1.feed(response)


findings = []
k = 4 # топ самых популярных поддеревьев

for path in sorted(parser1.needed_paths.items(), key=lambda item: item[1])[-k:]:
    true_path = path[0].split()
    parser2 = ForTableHTMLParser(true_path)
    parser2.feed(response)
    add_data = [i.strip() for i in parser2.data]
    findings.append(add_data)

print(findings) #нужная информация находятся в 0 и 3 поддереве

true_paths = []
for i, path in enumerate(sorted(parser1.needed_paths.items(), key=lambda item: item[1])[-4:]):
    if i == 0 or i == 3: # те поддеревья, которые нужны нам
        true_paths.append(path[0].split())

parser3 = ForDictHTMLParser(true_paths)
parser3.feed(response)
print(parser3.main_dict)


