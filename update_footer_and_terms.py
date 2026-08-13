import os
import re
import shutil

base_dir = 'c:/Users/legion-5pro/Documents/restie'

# 1. Update styles.css
css_path = os.path.join(base_dir, 'styles.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace the existing .site-footer block
old_footer_css = re.search(r'/\* ===== FOOTER ===== \*/.*?/\* Make logo black', css_content, flags=re.DOTALL)
new_footer_css = """/* ===== FOOTER ===== */
.site-footer {
    background: #4B3621;
    color: #fff;
    padding: 4rem 2rem 2rem;
    font-family: 'Inter', sans-serif;
}
.footer-grid {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
    gap: 2rem;
}
.footer-col--brand {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}
.footer-brand {
    font-family: 'Inter', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 0;
}
.footer-subscribe {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 300px;
}
.footer-subscribe input {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    padding: 0.8rem 1rem;
    color: #fff;
    font-family: 'Inter', sans-serif;
}
.footer-subscribe input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}
.footer-subscribe button {
    background: #FAF9F6;
    color: #4B3621;
    border: none;
    border-radius: 4px;
    padding: 0.8rem 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
    width: fit-content;
    font-family: 'Inter', sans-serif;
}
.footer-subscribe button:hover {
    background: #e8e6e1;
}
.footer-heading {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
    color: rgba(255, 255, 255, 0.9);
}
.footer-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.footer-list a {
    color: rgba(255, 255, 255, 0.7);
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.2s;
}
.footer-list a:hover {
    color: #fff;
}
.footer-social {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}
.footer-social a {
    color: #fff;
    opacity: 0.8;
    transition: opacity 0.2s;
}
.footer-social a:hover {
    opacity: 1;
}
.footer-bottom {
    max-width: 1200px;
    margin: 3rem auto 0;
    padding-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-copyright {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.7);
}
@media (max-width: 768px) {
    .footer-grid {
        grid-template-columns: 1fr 1fr;
    }
    .footer-col--brand {
        grid-column: 1 / -1;
        margin-bottom: 2rem;
    }
    .footer-bottom {
        flex-direction: column;
        text-align: center;
        gap: 1rem;
    }
}
@media (max-width: 480px) {
    .footer-grid {
        grid-template-columns: 1fr;
    }
}

/* Make logo black"""

if old_footer_css:
    css_content = css_content.replace(old_footer_css.group(0), new_footer_css)
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("Updated styles.css")

# 2. Update HTML files
html_files = [
    'index.html',
    'pillows/index.html',
    'cushions/index.html',
    'about/index.html',
    'checkout.html',
    'bulk/index.html',
    'mobile/index.html'
]

def get_footer_html(depth):
    prefix = '../' * depth
    if prefix == '':
        prefix = './'
        
    return f"""<!-- ===== FOOTER ===== -->
    <footer class="site-footer">
        <div class="footer-grid">
            <div class="footer-col footer-col--brand">
                <h2 class="footer-brand">REST NEST</h2>
                <form class="footer-subscribe" onsubmit="event.preventDefault();">
                    <input type="email" placeholder="Your email" required>
                    <button type="submit">SUBSCRIBE</button>
                </form>
                <div class="footer-social">
                    <a href="https://m.facebook.com/profile.php?id=61577983328975" target="_blank" aria-label="Facebook">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
                    </a>
                    <a href="https://www.instagram.com/restnest.in/" target="_blank" aria-label="Instagram">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
                    </a>
                </div>
            </div>
            <div class="footer-col">
                <h3 class="footer-heading">SHOP</h3>
                <ul class="footer-list">
                    <li><a href="{prefix}pillows/">Pillow</a></li>
                    <li><a href="{prefix}cushions/">Cushion</a></li>
                    <li><a href="{prefix}index.html">Shop All</a></li>
                    <li><a href="#">Sale Live 🔥</a></li>
                    <li><a href="#">New Launch</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h3 class="footer-heading">PARTNER</h3>
                <ul class="footer-list">
                    <li><a href="#">Become a Retailer</a></li>
                    <li><a href="#">Become a Dealer</a></li>
                    <li><a href="{prefix}bulk/">Place Your Bulk Order</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h3 class="footer-heading">HELP</h3>
                <ul class="footer-list">
                    <li><a href="#">Contact us</a></li>
                    <li><a href="#">Track Your Order</a></li>
                    <li><a href="#">FAQ's</a></li>
                    <li><a href="#">Return and Refund Policy</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h3 class="footer-heading">COMPANY</h3>
                <ul class="footer-list">
                    <li><a href="{prefix}about/">About us</a></li>
                    <li><a href="#">Privacy Policy</a></li>
                    <li><a href="{prefix}terms/">Terms and Conditions</a></li>
                    <li><a href="#">Shipping Policy</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="footer-copyright">
                &copy; 2026, Rest Nest. All rights reserved. Hari Shankar Trading Co.
            </div>
        </div>
    </footer>"""

for file in html_files:
    path = os.path.join(base_dir, file)
    if not os.path.exists(path):
        continue
    
    depth = file.count('/')
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_footer = re.search(r'<!-- ===== FOOTER ===== -->.*?</footer>', content, flags=re.DOTALL)
    if old_footer:
        content = content.replace(old_footer.group(0), get_footer_html(depth))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated footer in {file}")

# 3. Create terms/index.html
terms_dir = os.path.join(base_dir, 'terms')
os.makedirs(terms_dir, exist_ok=True)
terms_path = os.path.join(terms_dir, 'index.html')

terms_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms and Conditions | RestNest</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Great+Vibes&family=Inter:wght@300;400;500;600&family=Pinyon+Script&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css?v=17">
    <style>
        .terms-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 8rem 1.5rem 4rem;
            font-family: 'Inter', sans-serif;
            color: #4B3621;
        }}
        .terms-container h1 {{
            font-family: var(--font-serif);
            font-size: 3.5rem;
            font-weight: 300;
            text-align: center;
            margin-bottom: 3rem;
        }}
        .terms-container h2 {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
        }}
        .terms-container p {{
            font-size: 1rem;
            line-height: 1.8;
            margin-bottom: 1.5rem;
            color: #7a5c40;
        }}
        .terms-container a {{
            color: #4B3621;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="bg-texture" aria-hidden="true"></div>
    
    <!-- ===== UNIFIED PILL NAVIGATION ===== -->
    <nav id="pill-nav" class="pill-nav">
        <div class="pill-nav__inner">
            <button class="mobile-menu-toggle" id="mobile-menu-toggle" aria-label="Toggle menu" aria-expanded="false">
                <span class="mobile-menu-toggle__bar"></span>
                <span class="mobile-menu-toggle__bar"></span>
                <span class="mobile-menu-toggle__bar"></span>
            </button>
            <ul class="pill-nav__list">
                <li><a href="../index.html" class="main-nav__link">Home</a></li>
                <li><a href="../pillows/" class="main-nav__link">Pillow</a></li>
                <li><a href="../cushions/" class="main-nav__link">Cushion</a></li>
                <li><a href="../bulk/" class="main-nav__link">Bulk</a></li>
                <li><a href="../about/" class="main-nav__link">About us</a></li>
            </ul>
            <div class="pill-nav__logo">
                <a href="../" style="display: flex; align-items: center;">
                    <img src="../assets/logo-nav.png" alt="RestNest">
                </a>
            </div>
            <div class="pill-nav__utils">
                <a href="#" class="top-bar__link">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    SEARCH
                </a>
                <a href="#" class="top-bar__link">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                    ACCOUNT
                </a>
                <button class="top-bar__link cart-btn" style="background: none; border: none; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; color: inherit; font-family: inherit; font-size: inherit; text-transform: uppercase;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="9" cy="21" r="1"></circle>
                        <circle cx="20" cy="21" r="1"></circle>
                        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                    </svg>
                    CART
                </button>
            </div>
        </div>
    </nav>
    
    <div class="mobile-nav-curtain" id="mobile-nav-curtain">
        <div class="mobile-nav-curtain__inner">
            <a class="mobile-nav-curtain__link" href="../mobile/index.html">Home</a>
            <a class="mobile-nav-curtain__link" href="../pillows/">Pillow</a>
            <a class="mobile-nav-curtain__link" href="../cushions/">Cushion</a>
            <a class="mobile-nav-curtain__link" href="../bulk/">Bulk</a>
            <a class="mobile-nav-curtain__link" href="../about/">About Us</a>
        </div>
    </div>

    <div class="terms-container">
        <h1>Terms and Conditions</h1>
        <p>Welcome to RestNest.in! Before you explore and make a purchase on our ecommerce website, we kindly ask you to read and understand our Terms and Conditions. By using our website, you agree to comply with and be bound by the following terms. If you disagree with any part of these terms, please refrain from using our website.</p>
        
        <h2>1. Acceptance of Terms:</h2>
        <p>By accessing or using RestNest.in, you acknowledge that you have read, understood, and agreed to these Terms and Conditions. These terms apply to all users of the site, including without limitation users who are browsers, vendors, customers, merchants, and contributors of content.</p>
        
        <h2>2. Changes to Terms:</h2>
        <p>RestNest reserves the right to update, change, or replace any part of these Terms and Conditions at any time. It is your responsibility to check this page periodically for changes. Your continued use of the website following the posting of any changes constitutes acceptance of those changes.</p>
        
        <h2>3. Products and Pricing:</h2>
        <p>RestNest strives to provide accurate product information, pricing, and availability. However, we do not guarantee the accuracy or completeness of this information. We reserve the right to modify the contents of the website at any time, but we make no commitment to update any information.</p>
        <p>All prices are listed in the currency specified on the website and are subject to change without notice. RestNest reserves the right to modify or discontinue products without prior notice.</p>
        
        <h2>4. Orders and Payment:</h2>
        <p>When you place an order on RestNest.in, you agree to provide accurate and complete information. You are responsible for maintaining the confidentiality of your account and password. RestNest reserves the right to refuse any order, limit quantities, and terminate accounts at our discretion.</p>
        <p>We accept various forms of payment, including credit cards and other secure payment methods. By providing payment information, you represent and warrant that you have the right to use the payment method and authorize us to charge the provided payment method for the total amount of your purchase.</p>
        
        <h2>5. Shipping and Delivery:</h2>
        <p>RestNest aims to process and ship orders promptly. Delivery times may vary based on your location. We will make reasonable efforts to fulfill orders within the estimated delivery time provided, but we are not responsible for any delays beyond our control.</p>
        <p>Customers are responsible for providing accurate shipping information. In the event of incorrect shipping details, additional charges for redelivery or redirection may apply.</p>
        
        <h2>6. Returns and Exchanges:</h2>
        <p>Please review our Return Policy for detailed information on returning or exchanging products purchased from RestNest.in.</p>
        
        <h2>7. Intellectual Property:</h2>
        <p>All content on RestNest.in, including text, graphics, logos, images, and software, is the property of RestNest and is protected by international copyright laws. You may not use, reproduce, distribute, or create derivative works based on this content without explicit permission from RestNest.</p>
        
        <h2>8. Privacy Policy:</h2>
        <p>Your privacy is important to us. Please review our Privacy Policy to understand how we collect, use, and protect your personal information.</p>
        
        <h2>9. Governing Law:</h2>
        <p>These Terms and Conditions are governed by and construed in accordance with the laws of Panipat, Haryana Jurisdiction, and you agree to submit to the exclusive jurisdiction of the courts located within Panipat, Haryana.</p>
        
        <h2>10. Contact Information:</h2>
        <p>If you have any questions or concerns about these Terms and Conditions, please contact us at <a href="mailto:contact@restnest.in">contact@restnest.in</a> or at our number - +91 7404674889.</p>
        <p>Thank you for choosing RestNest.in. We appreciate your trust in us and look forward to providing you with a delightful shopping experience!</p>
    </div>

{get_footer_html(1)}

</body>
</html>
"""

with open(terms_path, 'w', encoding='utf-8') as f:
    f.write(terms_html)
print(f"Created {terms_path}")

