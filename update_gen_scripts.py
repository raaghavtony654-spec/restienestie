import os
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

for file in ['gen_pillows.py', 'gen_cushions.py']:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if 'def slugify' not in c:
        c = 'import re\ndef slugify(text):\n    text = text.lower()\n    text = re.sub(r"[^a-z0-9]+", "-", text)\n    return text.strip("-")\n' + c
    
    c = c.replace('<a href="#">', '<a href="../product/?id={slugify(p[\'title\'])}">')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)
