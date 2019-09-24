from bs4 import BeautifulSoup
import requests
import csv
import time
import pandas as pd

for n in range(100, 200):
   url = f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={n}'
   source = requests.get(url)
   data = source.text
   soup = BeautifulSoup(data, 'lxml')
   links = []
   for title in soup.find_all('a', class_='bookTitle'):
       links.append(title['href'])
   link_ser = pd.Series(links)
   link_ser.to_csv('best_books_list', header=False, mode='a', index=False)