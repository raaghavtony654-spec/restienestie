import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

all_products = {}

def process_script(filename, category):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the products array text
    start = content.find('products = [')
    end = content.find(']', start) + 1
    if start != -1 and end != -1:
        products_str = content[start+11:end]
        try:
            products_list = eval(products_str)
            for p in products_list:
                # generate id from title
                pid = slugify(p['title'])
                p['id'] = pid
                p['category'] = category
                p['description'] = "Experience unmatched comfort and support with our premium " + category.lower() + ", designed for deeper sleep and a refreshed you."
                p['sizes'] = [
                    {"label": "Standard", "desc": "(24\" x 16\")"},
                    {"label": "Queen", "desc": "(28\" x 18\")"}
                ]
                all_products[pid] = p
        except Exception as e:
            print("Error parsing", filename, e)

process_script('gen_pillows.py', 'Pillow')
process_script('gen_cushions.py', 'Cushion')

with open('assets/products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, indent=2)
print(f"Saved {len(all_products)} products to assets/products.json")
