import sys

with open('gen_cushions.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "header = header.replace('href=\"index.html\"" in line or "header = header.replace('href=\"#\" class=\"main-nav__link\" id=\"nav-home\"" in line:
        continue
    if "header = header.replace('href=\"pillows.html\"" in line or "header = header.replace('href=\"#\" class=\"main-nav__link\" id=\"nav-pillow\"" in line:
        continue
    new_lines.append(line)
    if "full_page = header + products_html + footer" in line:
        # insert before
        new_lines.insert(-1, "header = header.replace('href=\"#\" class=\"main-nav__link\" id=\"nav-home\"', 'href=\"../index.html\" class=\"main-nav__link\" id=\"nav-home\"')\n")
        new_lines.insert(-1, "header = header.replace('href=\"pillows/\" class=\"main-nav__link\" id=\"nav-pillow\"', 'href=\"../pillows/\" class=\"main-nav__link\" id=\"nav-pillow\"')\n")
        new_lines.insert(-1, "header = header.replace('href=\"cushions/\" class=\"main-nav__link\" id=\"nav-cushion\"', 'href=\"../cushions/\" class=\"main-nav__link\" id=\"nav-cushion\"')\n")

with open('gen_cushions.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
