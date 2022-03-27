from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def download_html(link:str) -> str:
    response = urlopen(link)
    headers = response.headers
    data = response.read()
    data_decoded = data.decode('utf-8')

    return headers, data_decoded


response_headers, html_doc = download_html('https://habr.com/ru/post/543760/')
soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify())
data_blocks = []

for i in soup.head.next_elements:
    html = i
    pure_text = i.get_text()
    if float(len(html)) and re.match(r'[А-Яа-я\d\n\s]+', pure_text):
            if float(len(pure_text)) / float(len(html)) > 0.8:
                data_blocks.append(pure_text)

print(data_blocks)



# dict_EN = []
# with open('english_words.txt', 'r') as f:
#      for word in f.readlines():
#          if re.match(r'\w\w+', word):
#              dict_EN.append(word.strip())





# soup = BeautifulSoup(response, 'html.parser')
# print(soup)
# print('___________')
# print(soup.find_all(['span', 'script']))
#
#
#
#
# response_headers, response = download_html('https://habr.com/ru/post/543760/')
#
# data_response = response.strip().split()
#
# parser = MyHTMLParser()
# parser.feed(response)
# raw_data = parser.data
# print('HERE')
# print(raw_data)
# print('HERE')
#
# token_pattern = re.compile(r'[\s][A-Za-zА-Яа-я][A-Za-zА-Яа-я]+[\s]')
# #token_pattern = re.compile(r'\b[A-Za-zА-Яа-я][A-Za-zА-Яа-я]+\b')
# raw_data = token_pattern.findall(raw_data)
# raw_data = [i.strip() for i in raw_data]
# print(raw_data)
#
# data_for_user = []
# dict_EN = []
#
# with open('english_words.txt', 'r') as f:
#     for word in f.readlines():
#         if re.match(r'\w\w+', word):
#             dict_EN.append(word.strip())
#
# for word in raw_data:
#     if not(re.match(r'[А-Яа-я]', word)):
#         if word in dict_EN:
#             data_for_user.append(word)
#     elif re.match(r'[А-Яа-я]', word):
#         data_for_user.append(word)
#
# print(float(len(''.join(data_for_user)))/float(len(''.join(data_response))))
