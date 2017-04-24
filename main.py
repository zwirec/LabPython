import re

import requests as r
from bs4 import BeautifulSoup

url_authors = 'http://mmcm.bmstu.ru/authors/'
html = r.get(url_authors).content.decode('utf-8')
soup = BeautifulSoup(html, "html.parser")


def get_articles_amount(url):
    author_page_url = url_authors + url
    author_page = r.get(author_page_url).content.decode('utf-8')
    author_soup = BeautifulSoup(author_page, "html.parser")

    author_name_list = []
    for i in author_soup.find_all('h4'):
        if i.parent.name == 'div':
            author_name_list = i.next.split()[:3]
            # Имя автора
    author_name = ' '.join(author_name_list)

    articles = author_soup.find_all('a', dict(href=re.compile("/articles/[0-9]+")))

    author_dict = {author_name: len(articles)}
    return author_dict


authors = []

for j in soup.find_all('a', dict(href=re.compile("/authors/.+"))):
    if j.parent.name == 'li':
        authors.append(get_articles_amount(j['href'].split('/')[2]))


def f(i):
    return list(i.values())[0]


authors.sort(key=f, reverse=True)

for i in range(9):
    for k, v in authors[i].items():
        print(k, v, sep=' ', end='\n')
