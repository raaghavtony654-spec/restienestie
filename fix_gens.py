import os

def fix_gen(filename, category):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Redefine products before the loop
    injection = f"""
import json
with open('assets/products.json', 'r', encoding='utf-8') as f:
    products_db = json.load(f)
products = [v for k, v in products_db.items() if v.get('category', '') == '{category}']

for idx, p in enumerate(products):"""
    
    content = content.replace("for idx, p in enumerate(products):", injection)
    
    # Replace btn_html
    btn_replacement = """    is_available = p.get('available', False)
    if is_available:
        btn_html = '<button class="add-to-cart-btn btn--primary" style="margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: pointer;">Add to Cart</button>'
    else:
        btn_html = '<button class="btn--primary" style="margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: not-allowed; opacity: 0.5;" disabled>Out of Stock</button>'
"""
    content = content.replace("    btn_html = '<button class=\"btn--primary\" style=\"margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: not-allowed; opacity: 0.5;\" disabled>Out of Stock</button>'", btn_replacement)
    
    # Fix the href slug and get_variant_id
    # Instead of slugify(p['title']), we use p['id']
    content = content.replace('href="../product/?id={slugify(p[\'title\'])}"', 'href="../product/?id={p[\'id\']}"')
    content = content.replace('get_variant_id_from_image(p[\'imgUrl\'])', "p.get('variantId', '')")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

fix_gen('gen_pillows.py', 'Pillow')
fix_gen('gen_cushions.py', 'Cushion')
print("Generators fixed.")
