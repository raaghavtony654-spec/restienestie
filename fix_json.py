import json
import os

base_dir = 'c:/Users/legion-5pro/Documents/restie'
json_path = os.path.join(base_dir, 'assets/products.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_images = [
    'assets/new_img_1.jpg',
    'assets/new_img_2.jpg',
    'assets/new_img_3.jpg',
    'assets/new_img_4.jpg',
    'assets/new_img_5.jpg'
]

img_idx = 0
for pid, product in data.items():
    # p['title'] or p['name']
    title = product.get('title', product.get('name', ''))
    if "Premium White Sleeping Pillow" in title:
        continue
        
    product['imgUrl'] = new_images[img_idx % len(new_images)]
    img_idx += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
    
print("Fixed products.json")
