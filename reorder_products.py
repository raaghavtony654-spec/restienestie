import json

with open('assets/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Update availability
target_pillow = "rest-nest-premium-white-sleeping-pillow-glace-cotton-fabric-lightweight-comfortable-pack-of-2"
target_cushion = "rest-nest-16x16-white-stripe-soft-cushions-pack-of-5"

if target_pillow in products:
    products[target_pillow]["available"] = True
if target_cushion in products:
    products[target_cushion]["available"] = False

# Reorder so target_pillow is at the top
new_products = {}
if target_pillow in products:
    new_products[target_pillow] = products[target_pillow]

for k, v in products.items():
    if k != target_pillow:
        new_products[k] = v

with open('assets/products.json', 'w', encoding='utf-8') as f:
    json.dump(new_products, f, indent=2)

print("Updated products.json")
