import os

files_to_update = [
    'c:/Users/legion-5pro/Documents/restie/checkout.html',
    'c:/Users/legion-5pro/Documents/restie/bulk/index.html'
]

for file_path in files_to_update:
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-16') as f:
                content = f.read()
                
        # Replace John and Doe
        new_content = content.replace('placeholder="John"', 'placeholder="Raj"')
        new_content = new_content.replace('placeholder="Doe"', 'placeholder="Gupta"')
        new_content = new_content.replace('placeholder="john@email.com"', 'placeholder="raj@email.com"')
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
