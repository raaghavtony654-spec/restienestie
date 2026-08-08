import json
import os

filepath = 'assets/products.json'
with open(filepath, 'r', encoding='utf-8') as f:
    products = json.load(f)

for k in products.keys():
    products[k]['available'] = False

new_id = "rest-nest-16x16-white-stripe-soft-cushions-pack-of-5"
products[new_id] = {
    "title": "Rest Nest 16x16 White Stripe Soft Cushions \u2013 Pack of 5",
    "imgUrl": "https://cdn.shopify.com/s/files/1/0603/5845/9453/files/1_d8e16e21-c6a8-49d1-b0aa-59f53cb3cc74.jpg?v=1755690481",
    "salePrice": "Rs. 1,270.00",
    "originalPrice": "Rs. 2,500.00", 
    "discount": "-49%",
    "id": new_id,
    "category": "Cushion",
    "description": "Experience unmatched comfort and support with our premium cushion, designed for deeper sleep and a refreshed you.",
    "sizes": [
      {
        "label": "Standard",
        "desc": "(16\" x 16\")"
      }
    ],
    "variantId": "gid://shopify/ProductVariant/42544518201405",
    "available": True
}

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2)

print("Updated products.json")
