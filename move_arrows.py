import re
import glob

# 1. Update index.html
with open('c:/Users/legion-5pro/Documents/restie/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(
    r'<div class="collection__container">\s*<h2 class="collection__heading">Top Selling Products</h2>\s*<div class="products-slider" id="products-slider">\s*<button class="slider-arrow slider-arrow--prev" id="slider-prev" aria-label="Previous">&larr;</button>\s*<button class="slider-arrow slider-arrow--next" id="slider-next" aria-label="Next">&rarr;</button>',
    '<div class="collection__container" style="position: relative;">\n<h2 class="collection__heading">Top Selling Products</h2>\n<button class="slider-arrow slider-arrow--prev" id="slider-prev" aria-label="Previous">&larr;</button>\n<button class="slider-arrow slider-arrow--next" id="slider-next" aria-label="Next">&rarr;</button>\n<div class="products-slider" id="products-slider">',
    html
)

with open('c:/Users/legion-5pro/Documents/restie/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update styles.css
with open('c:/Users/legion-5pro/Documents/restie/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'\.slider-arrow--prev \{\s*left: -22px;\s*\}', '.slider-arrow--prev { left: -10px; }', css)
css = re.sub(r'\.slider-arrow--next \{\s*right: -22px;\s*\}', '.slider-arrow--next { right: -10px; }', css)
# Since the container now includes the heading height, we move them down a bit to center them on the cards
css = re.sub(r'top: 40%;', 'top: 55%;', css)

with open('c:/Users/legion-5pro/Documents/restie/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Bump version
html_files = glob.glob('c:/Users/legion-5pro/Documents/restie/**/*.html', recursive=True)
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=14', content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
