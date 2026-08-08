import re
def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")
import json

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

products = [
    {
        "title": "Rest Nest 16x16 White Stripe Soft Cushions \u2013 Pack of 5",
        "imgUrl": "https://cdn.shopify.com/s/files/1/0603/5845/9453/files/1_d8e16e21-c6a8-49d1-b0aa-59f53cb3cc74.jpg?v=1755690481",
        "salePrice": "Rs. 1,270.00",
        "originalPrice": "Rs. 2,500.00",
        "discount": "-49%"
    },
    {
        "title": "Rest Nest Soft Cushion Pack Of 2 – Premium Recron Fiber (17x27 Inch)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_a6f3313d-a03b-4e75-81c5-b1b6cdf0e000.jpg?v=1755690677&width=720",
        "salePrice": "Rs. 1,065.00",
        "originalPrice": "Rs. 1,913.00",
        "discount": "-44%"
    },
    {
        "title": "Rest Nest Orthopedic Cervical Memory Foam Cushion – White (1 Pc)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_e843ed76-397f-41e8-ba42-ccad9e82bd12.jpg?v=1755686284&width=720",
        "salePrice": "Rs. 1,175.00",
        "originalPrice": "Rs. 2,229.00",
        "discount": "-47%"
    },
    {
        "title": "Rest Nest Slim Microfiber Cushion – 17x27 Inch, White 1 Pcs",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_b92871a1-943d-4257-b5f3-a86ff0eb0901.jpg?v=1755690027&width=720",
        "salePrice": "Rs. 1,014.00",
        "originalPrice": "Rs. 1,928.00",
        "discount": "-47%"
    },
    {
        "title": "Rest Nest Premium White Glace Cotton Cushions – Pack Of 2 (800g Each)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_92da7dc2-8045-451c-99f9-4743161a2420.jpg?v=1755689166&width=720",
        "salePrice": "Rs. 1,140.00",
        "originalPrice": "Rs. 2,504.00",
        "discount": "-54%"
    },
    {
        "title": "Rest Nest ContourCare™ Memory Foam Cushion – Orthopedic Support For Perfect Sleep",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_a2560cc8-5c8b-4a1d-ae3f-36de15dc65af.jpg?v=1755688418&width=720",
        "salePrice": "Rs. 1,175.00",
        "originalPrice": "Rs. 2,228.00",
        "discount": "-47%"
    },
    {
        "title": "Rest Nest White & Gold Glace Cotton Sleeping Cushions – Pack Of 2 (Lightweight, 750g Each)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_4df46894-3ca2-49df-bfa3-f01e50775aab.jpg?v=1755687611&width=720",
        "salePrice": "Rs. 1,110.00",
        "originalPrice": "Rs. 1,897.00",
        "discount": "-41%"
    },
    {
        "title": "Rest Nest Premium White Sleeping Cushion | Glace Cotton Fabric | Lightweight & Comfortable | Pack Of 2",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_d0746433-10cb-4f6c-8541-3d56f3bfa1ab.jpg?v=1755687154&width=720",
        "salePrice": "Rs. 1,063.00",
        "originalPrice": "Rs. 1,920.00",
        "discount": "-44%"
    },
    {
        "title": "Rest Nest Blue & White Polycotton Cushion – Pack Of 2 (16x26 Inch, Light Weight, Soft & Supportive, Filled With Reliance Recron Fiber)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_5ecdda45-68b7-4bdb-b2df-b11459a9ed22.jpg?v=1755685988&width=720",
        "salePrice": "Rs. 1,110.00",
        "originalPrice": "Rs. 1,897.00",
        "discount": "-41%"
    },
    {
        "title": "Rest Nest Premium Polycotton Cushion With Recron Fiber Filling – Black & White, 16x26 Inch (Pack Of 2)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_45de0a17-36f2-479d-85c5-ddc07b5466ee.jpg?v=1755684969&width=720",
        "salePrice": "Rs. 964.00",
        "originalPrice": "Rs. 1,928.00",
        "discount": "-50%"
    }
]

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# find header (everything until <!-- ===== HERO SLIDER ===== -->)
header_end = html.find('<!-- ===== HERO SLIDER ===== -->')
header = html[:header_end]

# find footer (from <div class="search-modal")
footer_start = html.find('<!-- ===== SEARCH MODAL ===== -->')

footer = html[footer_start:]

products_html = '<section class="page-header"><h1 style="text-align:center; font-family:var(--font-serif); font-size:3rem; font-weight:300; margin:10rem 0 4rem 0; color:#4B3621;">Our Cushion Collection</h1></section>'
sort_ui = """
<div class="sort-container" style="display: flex; justify-content: flex-end; margin-bottom: 2rem;">
    <label for="product-sort" style="margin-right: 1rem; align-self: center; font-family: var(--font-sans); font-size: 0.9rem;">Sort by:</label>
    <select id="product-sort" class="product-sort-select" style="padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; font-family: var(--font-sans); background: transparent;">
        <option value="most-selling">Most Selling</option>
        <option value="price-low">Price: Low to High</option>
        <option value="price-high">Price: High to Low</option>
        <option value="a-z">Alphabetical: A-Z</option>
        <option value="z-a">Alphabetical: Z-A</option>
    </select>
</div>
"""
products_html += '<section class="collection"><div class="collection__container">'
products_html += sort_ui
products_html += '<div class="products-grid" id="products-grid" style="display:grid; grid-template-columns:repeat(3, 1fr); gap:2rem;">'

for idx, p in enumerate(products):
    title = re.sub(r'^(Rest\s*Nest(?:\u2122)?\s*-?\s*)', '', p['title'], flags=re.IGNORECASE)
    price_val = float(p['salePrice'].replace('Rs. ', '').replace(',', ''))
    
    if "White Stripe Soft Cushions" in p['title']:
        btn_html = '<button class="add-to-cart-btn btn--primary" style="margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: pointer; transition: opacity 0.3s;" onmouseover="this.style.opacity=\'0.8\'" onmouseout="this.style.opacity=\'1\'">Add to Cart</button>'
    else:
        btn_html = '<button class="btn--primary" style="margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: not-allowed; opacity: 0.5;" disabled>Out of Stock</button>'
        
    products_html += f"""
    <div class="products-slider__card" style="margin-bottom: 2rem; position: relative;" data-price="{price_val}" data-title="{title}" data-order="{idx}" data-variant-id="{get_variant_id_from_image(p['imgUrl'])}">
        <a href="../product/?id={slugify(p['title'])}" style="text-decoration: none; color: inherit;">
            <span class="products-slider__badge">{p['discount']}</span>
            <div class="products-slider__img-wrap">
                <img src="{p['imgUrl']}" alt="{title}">
            </div>
            <h3 class="products-slider__name" style="white-space: normal; text-overflow: clip;">{title}</h3>
            <div class="products-slider__price">
                <span class="products-slider__sale">{p['salePrice']}</span>
                <span class="products-slider__original">{p['originalPrice']}</span>
            </div>
        </a>
        {btn_html}
    </div>
    """

products_html += '</div></div></section>'

# Make the home link point back to index.html
header = header.replace('href="#" class="main-nav__link" id="nav-cushion"', 'href="cushions.html" class="main-nav__link" id="nav-cushion"')

header = header.replace('href="#" class="main-nav__link" id="nav-home"', 'href="../index.html" class="main-nav__link" id="nav-home"')
header = header.replace('href="pillows/" class="main-nav__link" id="nav-pillow"', 'href="../pillows/" class="main-nav__link" id="nav-pillow"')
header = header.replace('href="cushions/" class="main-nav__link" id="nav-cushion"', 'href="../cushions/" class="main-nav__link" id="nav-cushion"')
header = header.replace('href="about/" class="main-nav__link" id="nav-about-us"', 'href="../about/" class="main-nav__link" id="nav-about-us"')
header = header.replace('<body class="landing-page">', '<body>')
header = header.replace('href="styles.css', 'href="../styles.css')
footer = footer.replace('src="shopify-integration.js"', 'src="../shopify-integration.js"')
footer = footer.replace('src="script.js', 'src="../script.js')
full_page = header + products_html + footer

with open('cushions/index.html', 'w', encoding='utf-8') as f:
    f.write(full_page)
