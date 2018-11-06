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

for month in months.keys():
  if not os.path.isdir("scrapper/files/%s" % (months[month]['number'],)):
    os.mkdir("scrapper/files/%s/" % (months[month]['number'],))

  days = [x for x in range(1, months[month]['days'] + 1)]

  for day in days:
    if not os.path.isdir("scrapper/files/%s/%s" % (months[month]['number'],day)):
      os.mkdir("scrapper/files/%s/%s/" % (months[month]['number'],day))

    url = 'https://efemerides20.com/%s' % (str(day) + '-de-' + month,)

    html = urlopen(url).read()

    page = BeautifulSoup(html, 'html.parser')

    ephemeris = [p.get_text().strip().replace(u'\xa0', u' ') for p in page.find_all('section', class_='efemeride-list')[0].find_all('p')]

    with open("scrapper/files/%s/%s/list.txt" % (months[month]['number'],day), 'w') as file:
      for line in ephemeris:
        file.write('%s\n' % line)
