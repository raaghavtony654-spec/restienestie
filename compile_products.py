import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# Mapping from image filename hash to correct Shopify variant ID
# These are the REAL variant IDs fetched from Shopify Storefront API
IMAGE_TO_VARIANT = {
    '1_a6f3313d-a03b-4e75-81c5-b1b6cdf0e000': 'gid://shopify/ProductVariant/42544537272381',  # Soft Pillow Pack of 2
    '1_e843ed76-397f-41e8-ba42-ccad9e82bd12': 'gid://shopify/ProductVariant/42544414785597',  # Orthopedic Cervical Memory Foam Pillow
    '1_b92871a1-943d-4257-b5f3-a86ff0eb0901': 'gid://shopify/ProductVariant/42544516202557',  # Slim Microfiber Pillow
    '1_92da7dc2-8045-451c-99f9-4743161a2420': 'gid://shopify/ProductVariant/42544497819709',  # Premium White Glace Cotton Pillows
    '1_a2560cc8-5c8b-4a1d-ae3f-36de15dc65af': 'gid://shopify/ProductVariant/42544459055165',  # ContourCare Memory Foam Pillow
    '1_4df46894-3ca2-49df-bfa3-f01e50775aab': 'gid://shopify/ProductVariant/42544433791037',  # White & Gold Glace Cotton Sleeping Pillows
    '1_d0746433-10cb-4f6c-8541-3d56f3bfa1ab': 'gid://shopify/ProductVariant/42544421371965',  # Premium White Sleeping Pillow
    '1_5ecdda45-68b7-4bdb-b2df-b11459a9ed22': 'gid://shopify/ProductVariant/42544411344957',  # Blue & White Polycotton Pillow
    '1_45de0a17-36f2-479d-85c5-ddc07b5466ee': 'gid://shopify/ProductVariant/42544398106685',  # Premium Polycotton Pillow Black & White
    '1_d8e16e21-c6a8-49d1-b0aa-59f53cb3cc74': 'gid://shopify/ProductVariant/42544518201405',  # 16x16 White Stripe Soft Cushions
    '1_a5057e16-0586-404f-b2dd-f864fd106ef9': 'gid://shopify/ProductVariant/42544508993597',  # 5 Premium White Cushions
    '1_56743c63-2af6-4227-bf0a-12aa212512fe': 'gid://shopify/ProductVariant/42544490250301',  # 16x16 White Premium Cushions
    '1_79a38007-2309-458b-b508-aab475956624': 'gid://shopify/ProductVariant/42544443424829',  # Soft Cushion Set of 5
    '1_024d103c-c62f-4258-acc5-68e61b231d6e': 'gid://shopify/ProductVariant/42544392765501',  # Premium Polycotton Cushions Blue
}

def get_variant_id_from_image(img_url):
    """Extract the image filename hash and look up the real variant ID."""
    # Match the unique part of the image filename (before .jpg)
    match = re.search(r'/(1_[a-f0-9\-]+)\.jpg', img_url)
    if match:
        key = match.group(1)
        if key in IMAGE_TO_VARIANT:
            return IMAGE_TO_VARIANT[key]
    return 'gid://shopify/ProductVariant/42544537272381'  # fallback

all_products = {}

def process_script(filename, category):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the products array text
    start = content.find('products = [')
    end = content.find(']', start) + 1
    if start != -1 and end != -1:
        products_str = content[start+11:end]
        try:
            products_list = eval(products_str)
            for p in products_list:
                # generate id from title
                pid = slugify(p['title'])
                p['id'] = pid
                p['category'] = category
                p['description'] = "Experience unmatched comfort and support with our premium " + category.lower() + ", designed for deeper sleep and a refreshed you."
                p['sizes'] = [
                    {"label": "Standard", "desc": "(24\" x 16\")"},
                    {"label": "Queen", "desc": "(28\" x 18\")"}
                ]
                # Look up the REAL variant ID based on image URL
                p['variantId'] = get_variant_id_from_image(p.get('imgUrl', ''))
                all_products[pid] = p
        except Exception as e:
            print("Error parsing", filename, e)

process_script('gen_pillows.py', 'Pillow')
process_script('gen_cushions.py', 'Cushion')

with open('assets/products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, indent=2)
print(f"Saved {len(all_products)} products to assets/products.json")

# Verify variant ID uniqueness
variant_ids = {}
for pid, p in all_products.items():
    vid = p['variantId']
    if vid not in variant_ids:
        variant_ids[vid] = []
    variant_ids[vid].append(p['title'][:50])

print("\nVariant ID mapping:")
for vid, titles in variant_ids.items():
    marker = "OK" if len(titles) <= 1 else "SHARED"
    for t in titles:
        print(f"  {marker} {vid[-5:]} -> {t}")
