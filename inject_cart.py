import os

html_files = [
    'pillows/index.html',
    'cushions/index.html',
    'product/index.html',
    'gen_product_template.py',
    'gen_pillows.py',
    'gen_cushions.py'
]

cart_link = """                <a href="#" class="top-bar__link" id="cart-link">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="9" cy="21" r="1"></circle>
                        <circle cx="20" cy="21" r="1"></circle>
                        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                    </svg>
                    CART
                </a>
                <a href="#" class="top-bar__link" id="order-link">"""

cart_sidebar = """    <!-- ===== CART SIDEBAR ===== -->
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

    <!-- ===== SEARCH MODAL ===== -->"""

for f in html_files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        changed = False
        
        if 'id="cart-link"' not in content:
            content = content.replace('<a href="#" class="top-bar__link" id="order-link">', cart_link)
            changed = True
            
        if 'id="cart-sidebar"' not in content:
            content = content.replace('<!-- ===== SEARCH MODAL ===== -->', cart_sidebar)
            changed = True
            
        if changed:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {f}")
