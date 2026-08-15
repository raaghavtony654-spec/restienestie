import os
import re
import json

registry = {}

for root, dirs, files in os.walk('c:/Users/legion-5pro/Documents/restie'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            names = re.findall(r'<h3 class="products-slider__name"[^>]*>(.*?)</h3>', content, re.IGNORECASE | re.DOTALL)
            prices = re.findall(r'<span class="products-slider__sale">(.*?)</span>', content, re.IGNORECASE)

            title_match = re.search(r'<h1 class="product-title"[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            price_match = re.search(r'<span class="sale-price"[^>]*>(.*?)</span>', content, re.IGNORECASE)

            if len(names) == len(prices):
                for n, p in zip(names, prices):
                    n_clean = n.strip().replace('&amp;', '&')
                    n_clean = re.sub(r'<[^>]+>', '', n_clean)
                    p_clean = p.replace('Rs.', '').replace(',', '').strip()
                    try:
                        p_val = float(p_clean)
                        registry[n_clean] = p_val
                    except ValueError:
                        pass
            
            if title_match and price_match:
                n_clean = title_match.group(1).strip().replace('&amp;', '&')
                n_clean = re.sub(r'<[^>]+>', '', n_clean)
                p_clean = price_match.group(1).replace('Rs.', '').replace(',', '').strip()
                try:
                    p_val = float(p_clean)
                    registry[n_clean] = p_val
                except ValueError:
                    pass

print(json.dumps(registry, indent=4))
