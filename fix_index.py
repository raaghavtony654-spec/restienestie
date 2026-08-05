import re

IMAGE_TO_VARIANT = {
    '1_a6f3313d-a03b-4e75-81c5-b1b6cdf0e000': 'gid://shopify/ProductVariant/42544537272381',  
    '1_e843ed76-397f-41e8-ba42-ccad9e82bd12': 'gid://shopify/ProductVariant/42544414785597',  
    '1_b92871a1-943d-4257-b5f3-a86ff0eb0901': 'gid://shopify/ProductVariant/42544516202557',  
    '1_92da7dc2-8045-451c-99f9-4743161a2420': 'gid://shopify/ProductVariant/42544497819709',  
    '1_a2560cc8-5c8b-4a1d-ae3f-36de15dc65af': 'gid://shopify/ProductVariant/42544459055165',  
    '1_4df46894-3ca2-49df-bfa3-f01e50775aab': 'gid://shopify/ProductVariant/42544433791037',  
    '1_d0746433-10cb-4f6c-8541-3d56f3bfa1ab': 'gid://shopify/ProductVariant/42544421371965',  
    '1_5ecdda45-68b7-4bdb-b2df-b11459a9ed22': 'gid://shopify/ProductVariant/42544411344957',  
    '1_45de0a17-36f2-479d-85c5-ddc07b5466ee': 'gid://shopify/ProductVariant/42544398106685',  
    '1_d8e16e21-c6a8-49d1-b0aa-59f53cb3cc74': 'gid://shopify/ProductVariant/42544518201405',  
    '1_a5057e16-0586-404f-b2dd-f864fd106ef9': 'gid://shopify/ProductVariant/42544508993597',  
    '1_56743c63-2af6-4227-bf0a-12aa212512fe': 'gid://shopify/ProductVariant/42544490250301',  
    '1_79a38007-2309-458b-b508-aab475956624': 'gid://shopify/ProductVariant/42544443424829',  
    '1_024d103c-c62f-4258-acc5-68e61b231d6e': 'gid://shopify/ProductVariant/42544392765501',  
}

def get_variant_id_from_image(img_url):
    match = re.search(r'/(1_[a-f0-9\-]+)\.jpg', img_url)
    if match:
        key = match.group(1)
        if key in IMAGE_TO_VARIANT:
            return IMAGE_TO_VARIANT[key]
    return 'gid://shopify/ProductVariant/42544537272381'

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

parts = html.split('<div class="products-slider__card"')
new_html = parts[0]

for i in range(1, len(parts)):
    part = parts[i]
    if 'data-variant-id=' in part[:100]:
        new_html += '<div class="products-slider__card"' + part
        continue
    
    img_match = re.search(r'<img[^>]+src="([^"]+)"', part)
    if img_match:
        img_url = img_match.group(1)
        variant_id = get_variant_id_from_image(img_url)
        new_html += f'<div class="products-slider__card" data-variant-id="{variant_id}"' + part
    else:
        new_html += '<div class="products-slider__card"' + part

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Fixed index.html!")
