import os
import glob

def fix_cart_badge():
    html_files = glob.glob('**/*.html', recursive=True)
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'cart-badge' in content and 'background-color: #4B3621;' in content:
            # Replace only in the context of the cart badge inline style
            new_content = content.replace(
                '<span class="cart-badge" style="background-color: #4B3621;',
                '<span class="cart-badge" style="background-color: #A67C52;'
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")

if __name__ == '__main__':
    fix_cart_badge()
