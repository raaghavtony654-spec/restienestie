import re
import json

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern: <a href="https://restnest.in/products/...">\s*<span class="products-slider__badge">.*?</span>\s*<div class="products-slider__img-wrap">.*?</div>\s*<h3 class="products-slider__name">(.*?)</h3>
# It's easier to find the <h3> title, then go backwards to replace the <a> tag.
# Let's split by '<div class="products-slider__card">'

parts = html.split('<div class="products-slider__card">')
for i in range(1, len(parts)):
    # Find title
    m = re.search(r'<h3 class="products-slider__name">(.*?)</h3>', parts[i])
    if m:
        title = m.group(1).strip()
        slug = slugify(title)
        # replace the href
        parts[i] = re.sub(r'<a href="[^"]*">', f'<a href="product/?id={slug}">', parts[i], count=1)

html = '<div class="products-slider__card">'.join(parts)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
