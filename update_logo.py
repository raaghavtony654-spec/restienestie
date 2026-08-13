import os
import glob
import re

css = """
/* Make logo black when not scrolled on pages other than home */
body:not(.page-home) .pill-nav:not(.scrolled) .pill-nav__logo img {
    filter: brightness(0);
}
"""

with open('c:/Users/legion-5pro/Documents/restie/styles.css', 'a', encoding='utf-8') as f:
    f.write("\n" + css + "\n")

html_files = glob.glob('c:/Users/legion-5pro/Documents/restie/**/*.html', recursive=True)

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=12', content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated CSS version in {file_path}")
