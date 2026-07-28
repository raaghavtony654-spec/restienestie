import re
import os

def px_to_rem(match):
    val_str = match.group(1)
    val = float(val_str)
    
    if val == 1:
        return "1px"  # Keep 1px for borders/outlines
    if val == 0:
        return "0"
        
    rem_val = val / 16.0
    # format to remove trailing zeros
    rem_str = f"{rem_val:.4f}".rstrip('0').rstrip('.')
    return f"{rem_str}rem"

filepath = 'styles.css'
with open(filepath, 'r', encoding='utf-8') as f:
    css = f.read()

# Add html root scaling rule if not present
root_css = "    font-size: clamp(10px, 1.11vw, 24px);\n"

if "html {\n" in css and "font-size: clamp" not in css:
    css = css.replace("html {\n", "html {\n" + root_css)
elif "html {" not in css:
    print("WARNING: html selector not found!")

# Replace all px
new_css = re.sub(r'(\d+(?:\.\d+)?)px', px_to_rem, css)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_css)

print("Successfully converted px to rem in styles.css!")
