import os
import re

base_dir = 'c:/Users/legion-5pro/Documents/restie'

html_files = [
    'index.html',
    'pillows/index.html',
    'cushions/index.html',
    'mobile/index.html'
]

new_images = [
    'assets/new_img_1.jpg',
    'assets/new_img_2.jpg',
    'assets/new_img_3.jpg',
    'assets/new_img_4.jpg',
    'assets/new_img_5.jpg'
]

img_idx = 0

for file in html_files:
    path = os.path.join(base_dir, file)
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace <img ... src="assets/..."> inside cards that DO NOT have "Premium White Sleeping Pillow"
    # Find all cards
    card_pattern = re.compile(r'(<div class="products-slider__card">)(.*?)(</div>\s*(?:<button.*?</button>\s*</div>|</div>\s*</div>))', re.DOTALL)
    
    def replacer(match):
        global img_idx
        start = match.group(1)
        inner = match.group(2)
        end = match.group(3)
        
        # If this is the available product, skip
        if "Premium White Sleeping Pillow" in inner:
            return match.group(0)
            
        # Replace the first <img src="..."> in `inner` with a new image
        # Also need to handle ../assets for nested folders
        prefix = '../' if '/' in file else ''
        new_src = prefix + new_images[img_idx % len(new_images)]
        
        # Simple string replacement for src="assets/..."
        # We find the img tag and replace its src
        inner = re.sub(r'src="[^"]+"', f'src="{new_src}"', inner, count=1)
        
        img_idx += 1
        
        return start + inner + end

    # Actually the end delimiter of a card can vary because some have <a> tags, some have <div>s, some have <button>.
    # So regex for full card is tricky. Let's just find all img tags and look ahead to the product name.
    # A better approach: 
    # Use re.split on '<div class="products-slider__card">'
    
    parts = content.split('<div class="products-slider__card">')
    new_parts = [parts[0]]
    
    for part in parts[1:]:
        if "Premium White Sleeping Pillow" in part:
            new_parts.append(part)
            continue
            
        # We need to replace the first src="..." in this part
        prefix = '../' if '/' in file else ''
        new_src = prefix + new_images[img_idx % len(new_images)]
        
        # Only replace the first image (which is the product image)
        new_part = re.sub(r'src="[^"]+"', f'src="{new_src}"', part, count=1)
        img_idx += 1
        new_parts.append(new_part)
        
    new_content = '<div class="products-slider__card">'.join(new_parts)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Updated images in {file}")

# Update products.json just in case
json_path = os.path.join(base_dir, 'assets/products.json')
with open(json_path, 'r', encoding='utf-8') as f:
    json_content = f.read()

import json
data = json.loads(json_content)
for i, p in enumerate(data):
    if "Premium White Sleeping Pillow" in p['name']:
        continue
    p['image'] = new_images[i % len(new_images)]

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
    
print("Updated products.json")
