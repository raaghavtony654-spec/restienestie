import re
def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")
import json

products = [
    {
        "title": "Rest Nest Soft Pillow Pack Of 2 – Premium Recron Fiber (17x27 Inch)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_a6f3313d-a03b-4e75-81c5-b1b6cdf0e000.jpg?v=1755690677&width=720",
        "salePrice": "Rs. 1,065.00",
        "originalPrice": "Rs. 1,913.00",
        "discount": "-44%"
    },
    {
        "title": "Rest Nest Orthopedic Cervical Memory Foam Pillow – White (1 Pc)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_e843ed76-397f-41e8-ba42-ccad9e82bd12.jpg?v=1755686284&width=720",
        "salePrice": "Rs. 1,175.00",
        "originalPrice": "Rs. 2,229.00",
        "discount": "-47%"
    },
    {
        "title": "Rest Nest Slim Microfiber Pillow – 17x27 Inch, White 1 Pcs",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_b92871a1-943d-4257-b5f3-a86ff0eb0901.jpg?v=1755690027&width=720",
        "salePrice": "Rs. 1,014.00",
        "originalPrice": "Rs. 1,928.00",
        "discount": "-47%"
    },
    {
        "title": "Rest Nest Premium White Glace Cotton Pillows – Pack Of 2 (800g Each)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_92da7dc2-8045-451c-99f9-4743161a2420.jpg?v=1755689166&width=720",
        "salePrice": "Rs. 1,140.00",
        "originalPrice": "Rs. 2,504.00",
        "discount": "-54%"
    },
    {
        "title": "Rest Nest ContourCare™ Memory Foam Pillow – Orthopedic Support For Perfect Sleep",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_a2560cc8-5c8b-4a1d-ae3f-36de15dc65af.jpg?v=1755688418&width=720",
        "salePrice": "Rs. 1,175.00",
        "originalPrice": "Rs. 2,228.00",
        "discount": "-47%"
    },
    {
        "title": "Rest Nest White & Gold Glace Cotton Sleeping Pillows – Pack Of 2 (Lightweight, 750g Each)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_4df46894-3ca2-49df-bfa3-f01e50775aab.jpg?v=1755687611&width=720",
        "salePrice": "Rs. 1,110.00",
        "originalPrice": "Rs. 1,897.00",
        "discount": "-41%"
    },
    {
        "title": "Rest Nest Premium White Sleeping Pillow | Glace Cotton Fabric | Lightweight & Comfortable | Pack Of 2",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_d0746433-10cb-4f6c-8541-3d56f3bfa1ab.jpg?v=1755687154&width=720",
        "salePrice": "Rs. 1,063.00",
        "originalPrice": "Rs. 1,920.00",
        "discount": "-44%"
    },
    {
        "title": "Rest Nest Blue & White Polycotton Pillow – Pack Of 2 (16x26 Inch, Light Weight, Soft & Supportive, Filled With Reliance Recron Fiber)",
        "imgUrl": "https://restnest.in/cdn/shop/files/1_5ecdda45-68b7-4bdb-b2df-b11459a9ed22.jpg?v=1755685988&width=720",
        "salePrice": "Rs. 1,110.00",
        "originalPrice": "Rs. 1,897.00",
        "discount": "-41%"
    },
    {
        "title": "Rest Nest Premium Polycotton Pillow With Recron Fiber Filling – Black & White, 16x26 Inch (Pack Of 2)",
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
footer_start = html.find('    <!-- ===== CART SIDEBAR ===== -->
    <div class="cart-overlay" id="cart-overlay"></div>
    <div class="cart-sidebar" id="cart-sidebar">
        <div class="cart-sidebar__header">
            <h2>Your Cart</h2>
            <button class="cart-sidebar__close" id="cart-close" aria-label="Close cart">&times;</button>
        </div>
        <div class="cart-sidebar__items" id="cart-items">
            <!-- Items will be injected here -->
            <p class="cart-empty-msg">Your cart is currently empty.</p>
        </div>
        <div class="cart-sidebar__footer">
            <div class="cart-sidebar__total">
                <span>Total:</span>
                <span id="cart-total-price">Rs. 0.00</span>
            </div>
            <a href="/cart.html" class="cart-sidebar__expand">Expand to Full Cart</a>
            <button class="cart-sidebar__checkout">Checkout</button>
        </div>
    </div>

    <!-- ===== SEARCH MODAL ===== -->')

footer = html[footer_start:]

products_html = '<section class="page-header"><h1 style="text-align:center; font-family:var(--font-serif); font-size:3rem; font-weight:300; margin:10rem 0 4rem 0;">Our Pillow Collection</h1></section>'
products_html += '<section class="collection"><div class="collection__container"><div class="products-grid" style="display:grid; grid-template-columns:repeat(3, 1fr); gap:2rem;">'

for p in products:
    products_html += f"""
    <div class="products-slider__card" style="margin-bottom: 2rem;">
        <a href="../product/?id={slugify(p['title'])}">
            <span class="products-slider__badge">{p['discount']}</span>
            <div class="products-slider__img-wrap">
                <img src="{p['imgUrl']}" alt="{p['title']}">
            </div>
            <h3 class="products-slider__name" style="white-space: normal; text-overflow: clip;">{p['title']}</h3>
            <div class="products-slider__price">
                <span class="products-slider__sale">{p['salePrice']}</span>
                <span class="products-slider__original">{p['originalPrice']}</span>
            </div>
        </a>
    </div>
    """

products_html += '</div></div></section>'

# Make the home link point back to index.html

header = header.replace('href="#" class="main-nav__link" id="nav-home"', 'href="../index.html" class="main-nav__link" id="nav-home"')
header = header.replace('href="pillows/" class="main-nav__link" id="nav-pillow"', 'href="../pillows/" class="main-nav__link" id="nav-pillow"')
header = header.replace('href="cushions/" class="main-nav__link" id="nav-cushion"', 'href="../cushions/" class="main-nav__link" id="nav-cushion"')
full_page = header + products_html + footer

with open('pillows/index.html', 'w', encoding='utf-8') as f:
    f.write(full_page)
