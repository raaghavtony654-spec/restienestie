import re
import glob

with open('c:/Users/legion-5pro/Documents/restie/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace left/right for desktop
css = re.sub(r'\.slider-arrow--prev \{ left: -10px; \}', '.slider-arrow--prev { left: 5px; }', css)
css = re.sub(r'\.slider-arrow--next \{ right: -10px; \}', '.slider-arrow--next { right: 5px; }', css)

# Remove the media query for 1024px since we are using 5px for everything 
css = re.sub(r'@media \(max-width: 1024px\) \{\s*\.slider-arrow--prev \{ left: 10px; \}\s*\.slider-arrow--next \{ right: 10px; \}\s*\}', '', css)

# Add container padding logic
padding_css = """
/* Make room for arrows on desktop */
#century-collection .collection__container {
    padding-left: 60px;
    padding-right: 60px;
}
@media (max-width: 900px) {
    #century-collection .collection__container {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
}
"""

if "Make room for arrows" not in css:
    css = css + "\n" + padding_css

with open('c:/Users/legion-5pro/Documents/restie/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Bump version
html_files = glob.glob('c:/Users/legion-5pro/Documents/restie/**/*.html', recursive=True)
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=15', content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
