import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Out of Stock button to products-slider__card if it doesn't have any button yet
parts = content.split('<div class="products-slider__card"')

out_of_stock_btn = '\n                        <button class="btn--primary" style="margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: not-allowed; opacity: 0.5;" disabled>Out of Stock</button>'

for i in range(1, len(parts)):
    # If this card doesn't already have a button (like the first one does)
    if '<button ' not in parts[i]:
        # Insert button before the closing </div> of the card
        # The closing </div> is right before the next <div class="products-slider__card" or at the end of the track
        # Actually, let's just insert it right after the closing </a> tag of the product link
        parts[i] = parts[i].replace('</a>\n                    </div>', f'</a>{out_of_stock_btn}\n                    </div>')

content = '<div class="products-slider__card"'.join(parts)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added out of stock buttons to index.html")
