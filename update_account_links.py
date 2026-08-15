import os
import re

for r, d, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(r, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            new_content = []
            for line in content.split('\n'):
                if 'id="account-link"' in line:
                    line = re.sub(r'href="[^"]*"', 'href="/account.html"', line)
                new_content.append(line)
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write('\n'.join(new_content))
            
print("Updated all account links")
