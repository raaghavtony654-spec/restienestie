import os

os.makedirs('product', exist_ok=True)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

header_end = html.find('<!-- ===== HERO SLIDER ===== -->')
header = html[:header_end]
header = header.replace('href="pillows/"', 'href="../pillows/"')
header = header.replace('href="cushions/"', 'href="../cushions/"')
header = header.replace('href="#" class="main-nav__link" id="nav-home"', 'href="../index.html" class="main-nav__link" id="nav-home"')
header = header.replace('href="styles.css"', 'href="../styles.css"')
header = header.replace('src="assets/', 'src="../assets/')

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
footer = footer.replace('src="script.js"', 'src="../script.js"')

product_html = """
    <!-- ===== PRODUCT PAGE ===== -->
    <section class="product-page">
        <div class="product-page__container">
            
            <!-- Left: Gallery -->
            <div class="product-gallery">
                <div class="product-gallery__thumbnails" id="product-thumbnails">
                    <!-- Thumbnails will be injected here -->
                </div>
                <div class="product-gallery__main">
                    <img id="product-main-image" src="" alt="Product Image">
                </div>
            </div>

            <!-- Right: Details -->
            <div class="product-details">
                <h1 class="product-details__title" id="product-title">Loading...</h1>
                
                <div class="product-details__reviews">
                    <div class="stars">
                        <svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        <svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                    </div>
                    <span class="reviews-count">4.8 (256 Reviews)</span>
                </div>

                <p class="product-details__desc" id="product-desc"></p>

                <div class="product-details__price-wrap">
                    <span class="price-sale" id="product-sale-price"></span>
                    <span class="price-original" id="product-original-price"></span>
                    <span class="price-badge" id="product-discount"></span>
                </div>

                <!-- Select Size -->
                <div class="product-options">
                    <h4 class="product-options__label">Select Size</h4>
                    <div class="product-options__grid" id="product-sizes">
                        <!-- Sizes will be injected here -->
                    </div>
                </div>

                <!-- Quantity -->
                <div class="product-quantity">
                    <h4 class="product-options__label">Quantity</h4>
                    <div class="quantity-selector">
                        <button id="qty-minus">&minus;</button>
                        <input type="number" id="qty-input" value="1" min="1">
                        <button id="qty-plus">&plus;</button>
                    </div>
                </div>

                <!-- Actions -->
                <div class="product-actions">
                    <button class="btn btn--primary" style="flex:1;">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:1.25rem; height:1.25rem; margin-right:0.5rem;"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
                        Add to Cart
                    </button>
                    <button class="btn btn--secondary" style="flex:1;">Buy Now</button>
                </div>

                <!-- Perks -->
                <div class="product-perks">
                    <div class="perk">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>
                        <div class="perk-text"><span>Free Shipping</span><br><small>On all orders</small></div>
                    </div>
                    <div class="perk">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                        <div class="perk-text"><span>30-Night Trial</span><br><small>Love it or return it</small></div>
                    </div>
                    <div class="perk">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                        <div class="perk-text"><span>1 Year Warranty</span><br><small>Quality assured</small></div>
                    </div>
                    <div class="perk">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
                        <div class="perk-text"><span>Easy Returns</span><br><small>Hassle-free returns</small></div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <!-- ===== FEATURES ===== -->
    <section class="engineered-features">
        <h2 class="engineered-features__heading">Engineered for Better Sleep</h2>
        <div class="engineered-features__grid">
            <div class="eng-feature">
                <div class="eng-feature__icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                </div>
                <div class="eng-feature__content">
                    <h4>Ergonomic Support</h4>
                    <p>Contours to your head and neck for perfect spinal alignment.</p>
                </div>
            </div>
            <div class="eng-feature">
                <div class="eng-feature__icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2v20M17 5l-10 14M22 12H2M19 17L5 7"></path></svg>
                </div>
                <div class="eng-feature__content">
                    <h4>Breathable & Cool</h4>
                    <p>Ventilated memory foam keeps you cool all night long.</p>
                </div>
            </div>
            <div class="eng-feature">
                <div class="eng-feature__icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>
                </div>
                <div class="eng-feature__content">
                    <h4>Hypoallergenic</h4>
                    <p>Resistant to dust mites, mold, and other allergens.</p>
                </div>
            </div>
            <div class="eng-feature">
                <div class="eng-feature__icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                </div>
                <div class="eng-feature__content">
                    <h4>Long Lasting Comfort</h4>
                    <p>High-quality foam retains shape and support for years.</p>
                </div>
            </div>
        </div>
    </section>
"""

full_page = header + product_html + footer

with open('product/index.html', 'w', encoding='utf-8') as f:
    f.write(full_page)
