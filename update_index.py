import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('assets/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Find each product card in index.html and update its link
# We can find the h3 tag and match it with our products
for pid, p in products.items():
    title = p['title']
    # The title might be slightly different or exact
    # In index.html, we have <h3 class="products-slider__name">TITLE</h3>
    # and right above it is the <a> tag.
    
    # Let's just use regex to replace all hrefs inside the product-slider__card
    pass

# Actually a simple regex to replace the hrefs in the slider:
# Since the products in top selling are just the first 10 pillows, let's just find all <a href="https://restnest.in/products/..."> and replace them with <a href="product/?id=..."> but wait, the ID is based on the title, not the Shopify URL slug.

import bs4
soup = bs4.BeautifulSoup(html, 'html.parser')
for card in soup.select('.products-slider__card'):
    a_tag = card.select_one('a')
    name_tag = card.select_one('.products-slider__name')
    if a_tag and name_tag:
        title = name_tag.text.strip()
        a_tag['href'] = f"product/?id={slugify(title)}"

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
