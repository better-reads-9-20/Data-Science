'''Script for scraping data from GoodReads.
--------------------------------------------
Uses rotating user agents and sleeping to try avoid getting blocked.
When blocked, sleeps for 30 seconds and tries again.

Prints out all values as it goes. This is just for watching that its collecting
the right data and can be commented out.'''

import csv
import time
from random import choice, randint

import pandas as pd
import requests
from bs4 import BeautifulSoup

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


# func to pick random from the list of user agents
def random_headers():
    return {'User-Agent': choice(desktop_agents), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

ser = pd.read_csv('bbl_4_ad')
vals = ser.values

csv_file = open('bb_details_1ad.csv', 'a')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['n', 'title', 'author', 'rating', 'num_ratings',
                     'num_reviews', 'descrip', 'isbn', 'isbn13',
                     'binding', 'edition', 'pages', 'published_on', 'genres'])
count = 0
for title in vals:
    n = title[0].split('.')[0].split('/')[-1]
    url = f'https://goodreads.com{title[0]}'
    print(url)
    time.sleep(randint(1, 5))
    source = requests.get(url, headers=random_headers())
    status = source.status_code

    if status == 403:
        time.sleep(30)
    elif source.ok:
        data = source.text
        soup = BeautifulSoup(data, 'lxml')
        try:
            title_div = soup.find('div', id='metacol')
            title = title_div.h1.text
            author = title_div.div.a.span.text
        except Exception:
            continue

        rating_div = title_div.find('div', id='bookMeta')
        rating = soup.find('span', itemprop='ratingValue').text
        num_rat_revs = rating_div.find_all('a', class_='gr-hyperlink')
        num_ratings = num_rat_revs[0].text
        num_reviews = num_rat_revs[1].text

        try:
            descrip = soup.find('div', id='description').find_all('span')[1].text
        except Exception:
            descrip = None

        details = soup.find('div', id='details').find_all('div', class_='row')
        try:
            binding = details[0].find('span', itemprop='bookFormat').text
        except Exception:
            binding = None
        try:
            edition = details[0].find('span', itemprop='bookEdition').text
        except Exception:
            edition = None
        try:
            pages = details[0].find('span', itemprop='numberOfPages').text
        except Exception:
            pages = None

        try:
            published_on = details[1].text
        except Exception:
            published_on = None
        genres = []
        genre_list = soup.find_all('a', class_='actionLinkLite bookPageGenreLink')
        for l in range(len(genre_list)):
            genres.append(genre_list[l].text)

        isbn = None
        isbn13 = None
        try:
            info = soup.find('div', id='bookDataBox', class_='uitext')
            #print(info)
            row_title = info.find_all('div', class_='infoBoxRowTitle')
            #print(row_title)
            row_item = info.find_all('div', class_='infoBoxRowItem')
            #print(row_item)
            
            for each in zip(row_title, row_item):
                #print(each[0], each[1])
                if each[0].text == 'ISBN':
                    isbn_info = each[1].text.split()
                    isbn = isbn_info[0]
                    isbn13 = isbn_info[-1]
        except Exception:
            continue
        csv_writer.writerow([n, title, author, rating, num_ratings,
                             num_reviews, descrip, isbn, isbn13,
                            binding, edition, pages, published_on, genres])
        print(isbn, isbn13)
        count += 1
        print(count)
    else:
        continue
