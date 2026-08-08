import os
import glob
import re

html_files = glob.glob('**/*.html', recursive=True)
old_url = 'https://restnest.in/cdn/shop/files/1_d0746433-10cb-4f6c-8541-3d56f3bfa1ab.jpg?v=1755687154&width=720'

for p in html_files:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace image URL
    new_url = '../assets/product-img-1.jpg' if '/' in p or '\\' in p else 'assets/product-img-1.jpg'
    content = content.replace(old_url, new_url)
    
    # Replace CSS version
    content = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=6', content)
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(html_files)} HTML files.")
