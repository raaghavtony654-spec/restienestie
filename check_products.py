from bs4 import BeautifulSoup
import os

base_dir = 'c:/Users/legion-5pro/Documents/restie'
path = os.path.join(base_dir, 'index.html')

with open(path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

cards = soup.find_all('div', class_='products-slider__card')
for card in cards:
    name_tag = card.find('h3', class_='products-slider__name')
    if not name_tag:
        continue
    name = name_tag.text.strip()
    
    oos = card.find('button', string=lambda t: t and 'Out of Stock' in t)
    
    if oos:
        print(f"OUT OF STOCK: {name}")
    else:
        print(f"AVAILABLE: {name}")
