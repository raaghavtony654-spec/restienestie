import glob
import re

css_path = 'c:/Users/legion-5pro/Documents/restie/styles.css'

try:
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
except UnicodeDecodeError:
    with open(css_path, 'r', encoding='utf-16') as f:
        css = f.read()

fix_css = """
@media (max-width: 900px) {
    .pill-nav__logo img {
        height: 26px !important;
    }
}
"""

if "height: 26px !important" not in css:
    css += "\n" + fix_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# Bump version to v=16
html_files = glob.glob('c:/Users/legion-5pro/Documents/restie/**/*.html', recursive=True)
for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-16') as f:
            content = f.read()
            
    new_content = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=16', content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
