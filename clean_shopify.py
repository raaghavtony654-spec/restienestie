import os
import re
import json

base_dir = r"c:\Users\legion-5pro\Documents\restie"

# 1. Clean HTML files
html_files = [
    "index.html",
    "mobile/index.html",
    "product/index.html",
    "pillows/index.html",
    "cushions/index.html",
    "about/index.html",
]

for rel_path in html_files:
    file_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove script tag for shopify-integration.js
    content = re.sub(r'<script src="(\.\./)?shopify-integration\.js"></script>\n?', '', content)
    
    # Remove data-variant-id attributes
    content = re.sub(r'\s*data-variant-id="gid://shopify/ProductVariant/\d+"', '', content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Cleaned {rel_path}")

# 2. Clean script.js
script_path = os.path.join(base_dir, "script.js")
if os.path.exists(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        script = f.read()
    
    # Remove Shopify sync blocks in qty-minus
    script = re.sub(r'// Sync with Shopify\s+if \(typeof ShopifyCart !== \'undefined\'.*?}\s+}', '', script, flags=re.DOTALL)
    
    # Replace ShopifyCart.goToCheckout() in buy now button
    script = script.replace('ShopifyCart.goToCheckout();', "window.location.href = basePath + 'checkout.html';")
    script = script.replace('await ShopifyCart.addItem(product.variantId, qty);', '')
    
    # Replace checkoutBtn logic
    checkout_logic = """if (typeof ShopifyCart !== 'undefined' && ShopifyCart.isConfigured()) {
                ShopifyCart.goToCheckout();
            } else {
                alert('Shopify checkout is not configured yet. Please set your store credentials in shopify-integration.js');
            }"""
    script = script.replace(checkout_logic, "window.location.href = basePath + 'checkout.html';")

    # Clean add to cart
    script = re.sub(r'const variantId = card\.getAttribute\(\'data-variant-id\'\) \|\| .*?;', '', script)
    script = re.sub(r'variantId: variantId', '', script)
    script = re.sub(r', variantId\s*}', ' }', script)
    
    script = re.sub(r'if \(typeof ShopifyCart !== \'undefined\' && variantId\) \{\s*ShopifyCart\.addItem\(variantId, qty\);\s*\}', '', script, flags=re.DOTALL)

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
    print("Cleaned script.js")

# 3. Clean mobile/index.html inline script (similar to script.js)
mobile_path = os.path.join(base_dir, "mobile", "index.html")
if os.path.exists(mobile_path):
    with open(mobile_path, "r", encoding="utf-8") as f:
        mobile = f.read()
        
    mobile = re.sub(r'// Sync with Shopify\s+if \(typeof ShopifyCart !== \'undefined\'.*?}\s+}', '', mobile, flags=re.DOTALL)
    mobile = mobile.replace('ShopifyCart.goToCheckout();', "window.location.href = '../checkout.html';")
    mobile = mobile.replace('await ShopifyCart.addItem(product.variantId, qty);', '')
    
    checkout_logic_mobile = """if (typeof ShopifyCart !== 'undefined' && ShopifyCart.isConfigured()) {
                ShopifyCart.goToCheckout();
            } else {
                alert('Shopify checkout is not configured yet. Please set your store credentials in shopify-integration.js');
            }"""
    mobile = mobile.replace(checkout_logic_mobile, "window.location.href = '../checkout.html';")

    mobile = re.sub(r'const variantId = card\.getAttribute\(\'data-variant-id\'\) \|\| .*?;', '', mobile)
    mobile = re.sub(r', variantId\s*}', ' }', mobile)
    mobile = re.sub(r'if \(typeof ShopifyCart !== \'undefined\' && variantId\) \{\s*ShopifyCart\.addItem\(variantId, qty\);\s*\}', '', mobile, flags=re.DOTALL)

    with open(mobile_path, "w", encoding="utf-8") as f:
        f.write(mobile)
    print("Cleaned mobile/index.html inline script")

# 4. Clean products.json
products_json = os.path.join(base_dir, "assets", "products.json")
if os.path.exists(products_json):
    with open(products_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for key, product in data.items():
        if "variantId" in product:
            del product["variantId"]
            
    with open(products_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Cleaned products.json")
