import re

file_path = 'c:/Users/legion-5pro/Documents/restie/bulk/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to remove everything from the old "Place Order" button down to the closing secure-badge div
pattern = r'<button type="submit" form="checkout-form" class="pay-btn" id="pay-btn">.*?</svg>\s*Secure checkout · SSL encrypted\s*</div>'

new_content = re.sub(pattern, '', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
