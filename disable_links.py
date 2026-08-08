import os
import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

for p in html_files:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Out of Stock' in content:
        # Replace <a href="..."> tags that contain "Out of Stock" with <div...>
        # We need to match <a href="product/?id=..."> ... Out of Stock ... </a>
        # Using a regex that finds the wrapping <a> tag for product cards
        
        # Product cards are typically structured like:
        # <a href="product/?id=..." style="...">
        #   ...
        #   Out of Stock
        #   ...
        # </a>
        
        new_content = re.sub(
            r'<a href="(?:\.\./)?product/\?id=[^"]*"([^>]*)>(.*?)</a>(\s*<button[^>]*>Out of Stock</button>)',
            r'<div\1>\2</div>\3',
            content,
            flags=re.DOTALL
        )
        
        if new_content != content:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {p}")
