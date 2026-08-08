import os
import glob
import re

def bump_css_version():
    html_files = glob.glob('**/*.html', recursive=True)
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace styles.css?v=X with styles.css?v=4
        # Or ../styles.css?v=X with ../styles.css?v=4
        new_content = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=4', content)
        
        # In case some don't have a version yet
        new_content = re.sub(r'href="(\.\./)?styles\.css"', r'href="\1styles.css?v=4"', new_content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated CSS version in {file_path}")

if __name__ == '__main__':
    bump_css_version()
