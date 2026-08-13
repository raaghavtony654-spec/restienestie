import os
import re

base_dir = 'c:/Users/legion-5pro/Documents/restie'

html_files = [
    'index.html',
    'pillows/index.html',
    'cushions/index.html',
    'mobile/index.html'
]

# We need to find the specific product card that starts with <a href="..."> and ends with </a>, 
# and contains "White &amp; Gold Glace Cotton Pillows" (or similar) and "1,110.00".
# And then replace the <a href="..."> with <div style="; text-decoration: none; color: inherit; cursor: default;">
# and replace </a> with </div> \n <button class="btn--primary" disabled="" style="margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: not-allowed; opacity: 0.5;">Out of Stock</button>

pattern = re.compile(
    r'<a href="[^"]*white-amp-gold-glace-cotton-pillows-pack-of-2[^"]*"(.*?)>(.*?)White\s*(?:&amp;|&)\s*Gold.*?1,110\.00.*?</a>',
    re.DOTALL | re.IGNORECASE
)

oos_button = '<button class="btn--primary" disabled="" style="margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: not-allowed; opacity: 0.5;">Out of Stock</button>'

for file in html_files:
    path = os.path.join(base_dir, file)
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if this specific card has an <a> tag wrapping it.
    def replacer(match):
        inner_content = match.group(2) + "White &amp; Gold" + match.group(0).split("White &amp; Gold")[1][:-4] 
        # Actually it's safer to just replace the <a> tags without altering inner text completely.
        original_match = match.group(0)
        # Find the first > to replace the opening tag
        first_gt = original_match.find('>')
        inner = original_match[first_gt+1:-4] # slice off </a>
        return f'<div style="; text-decoration: none; color: inherit; cursor: default;">{inner}</div>\n{oos_button}'

    new_content = pattern.sub(replacer, content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Processed {file}")
