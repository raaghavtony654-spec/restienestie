from bs4 import BeautifulSoup
import glob
import os

html_files = glob.glob('**/*.html', recursive=True)
count = 0

for p in html_files:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Out of Stock' not in content:
        continue
        
    soup = BeautifulSoup(content, 'html.parser')
    modified = False
    
    # Find all product cards
    for card in soup.find_all('div', class_='products-slider__card'):
        # Check if it has an out of stock button
        btn = card.find('button', string=lambda t: t and 'Out of Stock' in t)
        if btn:
            # It's out of stock! Find the <a> tag and change it to <div>
            a_tag = card.find('a')
            if a_tag and a_tag.has_attr('href'):
                a_tag.name = 'div'
                del a_tag['href']
                # Add inline styles to keep it looking the same
                a_tag['style'] = a_tag.get('style', '') + '; text-decoration: none; color: inherit; cursor: default;'
                modified = True
                
    if modified:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {p}")
        count += 1

print(f"Updated {count} files.")
