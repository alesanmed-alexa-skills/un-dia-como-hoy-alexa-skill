from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

months = {
    "enero": {
        "number": 1,
        "days": 31
    },
    "febrero": {
        "number": 2,
        "days": 28
    },
    "marzo": {
        "number": 3,
        "days": 31
    },
    "abril": {
        "number": 4,
        "days": 30
    },
    "mayo": {
        "number": 5,
        "days": 31
    },
    "junio": {
        "number": 6,
        "days": 30
    },
    "julio": {
        "number": 7,
        "days": 31
    },
    "agosto": {
        "number": 8,
        "days": 31
    },
    "septiembre": {
        "number": 9,
        "days": 30
    },
    "octubre": {
        "number": 10,
        "days": 31
    },
    "noviembre": {
        "number": 11,
        "days": 30
    },
    "diciembre": {
        "number": 12,
        "days": 31
    }
}

date = '2-de-enero'

date_parts = date.split('-')

path = 'files/{}/{}/list.txt'.format(
    months[date_parts[-1]]['number'], 
    date_parts[0])

url = 'https://efemerides20.com/{}'.format(date)

html = urlopen(url).read().decode('utf-8', errors='ignore').replace(u'\u200b', ' ')

page = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

ephemeris = [p.get_text().strip().replace(u'\xa0', u' ') for p in page.find_all(
    'section', class_='efemeride-list')[0].find_all('p')]

with open(path, 'w', encoding='utf-8') as file:
    for line in ephemeris:
        file.write('%s\n' % line)
