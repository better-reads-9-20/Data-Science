'''Script for scraping data from GoodReads.
--------------------------------------------
Uses rotating user agents and sleeping to try avoid getting blocked.
When blocked, sleeps for 30 seconds and tries again.

Prints out all values as it goes. This is just for watching that its collecting
the right data and can be commented out.'''

from bs4 import BeautifulSoup
import requests
import csv
import time
from random import choice, randint
import pandas as pd

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

pages = pd.read_csv('4K_isbn_list.csv', header=None)
vals = pages[1].values
print(len(vals))
csv_file = open('4K_missing_isbn.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['n', 'isbn', 'isbn13'])
count = 0
for n in vals[2000:]:
    url = f'https://goodreads.com/book/show/{n}'
    print(url)
    time.sleep(randint(1, 5))
    source = requests.get(url, headers=random_headers())
    status = source.status_code

    if status == 403:
        print('blocked')
        time.sleep(30)
    elif source.ok:
        print('In')
        data = source.text
        soup = BeautifulSoup(data, 'lxml')
        isbn = None
        isbn13 = None 
        try:
            info = soup.find('div', id='bookDataBox', class_='uitext')
            row_title = info.find_all('div', class_='infoBoxRowTitle')
            row_item = info.find_all('div', class_='infoBoxRowItem')
            for each in zip(row_title, row_item):
                if each[0].text == 'ISBN':
                    isbn_info = each[1].text.split()
                    isbn = isbn_info[0]
                    isbn13 = isbn_info[-1]
                elif each[0].text == 'ASIN':
                    isbn_info = each[1].text.split()
                    isbn = isbn_info[0]
                    isbn13 = None
        except Exception:
            continue
        print(n)
        print(isbn)
        print(isbn13)
        csv_writer.writerow([n, isbn, isbn13])
        count += 1
        print(count)
    else:
        print('hmmm')
        continue
