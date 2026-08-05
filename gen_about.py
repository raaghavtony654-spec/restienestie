import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract header and footer
header_end = html.find('<!-- ===== HERO SLIDER ===== -->')
header = html[:header_end]

footer_start = html.find('<!-- ===== SEARCH MODAL ===== -->')
footer = html[footer_start:]

about_html = """
<section class="page-header">
    <h1 style="text-align:center; font-family:var(--font-serif); font-size:3.5rem; font-weight:300; margin:8rem 0 1rem 0; color:#4B3621;">About RestNest</h1>
    <p style="text-align:center; font-family:var(--font-sans); font-size:1.25rem; font-weight:400; color:#7a5c40; margin-bottom:4rem;">Where Comfort Meets Timeless Design</p>
</section>

<section class="about-section" style="padding: 4rem 1rem; max-width: 800px; margin: 0 auto; text-align: center;">
    <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
        At RestNest, we believe every home deserves furniture that feels as good as it looks. We create thoughtfully designed pieces that combine comfort, durability, and modern aesthetics, helping you transform everyday spaces into places you'll love coming home to.
    </p>
    <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
        Whether you're furnishing a new home or refreshing your favorite corner, our collections are crafted to bring warmth, elegance, and functionality into every room.
    </p>
</section>

<section class="about-section" style="padding: 4rem 1rem; background-color: #FAF9F6; text-align: center;">
    <div style="max-width: 800px; margin: 0 auto;">
        <h2 style="font-family:var(--font-serif); font-size:2.5rem; font-weight:300; margin-bottom:2rem; color:#4B3621;">Our Story</h2>
        <h3 style="font-family:var(--font-serif); font-size:1.5rem; font-style:italic; margin-bottom:2rem; color:#7a5c40;">Every great home begins with furniture that reflects the people who live in it.</h3>
        <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
            RestNest was founded with a simple vision—to make premium-quality furniture accessible without compromising on design or craftsmanship. We work with skilled artisans, trusted manufacturers, and carefully selected materials to create products that are built for everyday living and made to last.
        </p>
        <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
            From contemporary designs to timeless classics, every collection is developed with attention to detail, ensuring beauty, comfort, and reliability in every piece.
        </p>
    </div>
</section>

<section class="about-section" style="padding: 4rem 1rem; max-width: 800px; margin: 0 auto; text-align: center;">
    <h2 style="font-family:var(--font-serif); font-size:2.5rem; font-weight:300; margin-bottom:2rem; color:#4B3621;">Our Mission</h2>
    <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
        Our mission is to create furniture that enhances everyday life by blending exceptional craftsmanship, functional design, and lasting quality.
    </p>
    <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
        We strive to deliver products that make homes more inviting while providing a seamless shopping experience from selection to delivery.
    </p>
</section>

<section class="about-section" style="padding: 4rem 1rem; background-color: #FAF9F6; text-align: center;">
    <div style="max-width: 800px; margin: 0 auto;">
        <h2 style="font-family:var(--font-serif); font-size:2.5rem; font-weight:300; margin-bottom:2rem; color:#4B3621;">Our Vision</h2>
        <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
            To become one of India's most trusted furniture brands by inspiring beautiful living spaces through innovative designs, premium quality, and customer-first service.
        </p>
    </div>
</section>

<section class="about-section" style="padding: 4rem 1rem; max-width: 1200px; margin: 0 auto;">
    <h2 style="font-family:var(--font-serif); font-size:2.5rem; font-weight:300; margin-bottom:3rem; color:#4B3621; text-align: center;">What Makes Us Different</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; text-align: center;">
        <div>
            <h3 style="font-family:var(--font-sans); font-size:1.25rem; font-weight:600; margin-bottom:1rem; color:#4B3621;">Premium Craftsmanship</h3>
            <p style="font-size: 1rem; line-height: 1.6; color: #7a5c40;">Every product is thoughtfully designed and manufactured using carefully selected materials for lasting durability and comfort.</p>
        </div>
        <div>
            <h3 style="font-family:var(--font-sans); font-size:1.25rem; font-weight:600; margin-bottom:1rem; color:#4B3621;">Modern & Timeless Designs</h3>
            <p style="font-size: 1rem; line-height: 1.6; color: #7a5c40;">Our collections are created to complement a variety of interior styles, ensuring they remain stylish for years to come.</p>
        </div>
        <div>
            <h3 style="font-family:var(--font-sans); font-size:1.25rem; font-weight:600; margin-bottom:1rem; color:#4B3621;">Quality You Can Trust</h3>
            <p style="font-size: 1rem; line-height: 1.6; color: #7a5c40;">Each piece undergoes rigorous quality checks before reaching your home, ensuring exceptional standards in every detail.</p>
        </div>
        <div>
            <h3 style="font-family:var(--font-sans); font-size:1.25rem; font-weight:600; margin-bottom:1rem; color:#4B3621;">Customer-Centric Experience</h3>
            <p style="font-size: 1rem; line-height: 1.6; color: #7a5c40;">From browsing to delivery and after-sales support, we're committed to making every step of your journey simple, transparent, and enjoyable.</p>
        </div>
    </div>
</section>

<section class="about-section" style="padding: 4rem 1rem; background-color: #FAF9F6;">
    <div style="max-width: 800px; margin: 0 auto;">
        <h2 style="font-family:var(--font-serif); font-size:2.5rem; font-weight:300; margin-bottom:3rem; color:#4B3621; text-align: center;">Our Values</h2>
        <ul style="list-style: none; padding: 0; font-size: 1.125rem; line-height: 2; color: #4B3621;">
            <li style="margin-bottom: 1rem;"><strong>Quality First</strong> – We never compromise on materials or craftsmanship.</li>
            <li style="margin-bottom: 1rem;"><strong>Customer Commitment</strong> – Your satisfaction is at the heart of everything we do.</li>
            <li style="margin-bottom: 1rem;"><strong>Honest Practices</strong> – Transparency and trust guide every decision.</li>
            <li style="margin-bottom: 1rem;"><strong>Innovation</strong> – We continuously improve our designs to meet evolving lifestyles.</li>
            <li style="margin-bottom: 1rem;"><strong>Sustainability</strong> – We strive to make responsible choices in sourcing and manufacturing whenever possible.</li>
        </ul>
    </div>
</section>

<section class="about-section" style="padding: 4rem 1rem; max-width: 800px; margin: 0 auto; text-align: center;">
    <h2 style="font-family:var(--font-serif); font-size:2.5rem; font-weight:300; margin-bottom:2rem; color:#4B3621;">Bringing Homes to Life</h2>
    <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
        Furniture is more than décor—it's where conversations begin, families gather, memories are created, and comfort becomes a part of everyday life.
    </p>
    <p style="font-size: 1.125rem; line-height: 1.8; color: #4B3621; margin-bottom: 2rem;">
        At RestNest, we're proud to be part of those moments by offering furniture that combines thoughtful design, dependable quality, and lasting comfort for modern homes.
    </p>
</section>

<section class="about-section" style="padding: 6rem 1rem; background-color: #4B3621; color: #FFF; text-align: center;">
    <div style="max-width: 800px; margin: 0 auto;">
        <h2 style="font-family:var(--font-serif); font-size:3rem; font-weight:300; margin-bottom:2rem; color:#FFF;">Build Your Perfect Space with RestNest</h2>
        <p style="font-size: 1.25rem; line-height: 1.8; color: rgba(255,255,255,0.8); margin-bottom: 3rem;">
            Discover furniture designed to elevate every room with style, comfort, and functionality. Explore our collections and find pieces that make your house truly feel like home.
        </p>
        <a href="../" class="cta-button" style="display: inline-block; padding: 1rem 2.5rem; background: transparent; border: 1px solid #FFF; color: #FFF; text-decoration: none; font-family: var(--font-sans); font-size: 0.875rem; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase;">Explore Our Collections</a>
    </div>
</section>
"""

header = header.replace('href="#" class="main-nav__link" id="nav-home"', 'href="../index.html" class="main-nav__link" id="nav-home"')
header = header.replace('href="pillows/" class="main-nav__link" id="nav-pillow"', 'href="../pillows/" class="main-nav__link" id="nav-pillow"')
header = header.replace('href="cushions/" class="main-nav__link" id="nav-cushion"', 'href="../cushions/" class="main-nav__link" id="nav-cushion"')
header = header.replace('href="about/" class="main-nav__link" id="nav-about-us"', 'href="../about/" class="main-nav__link" id="nav-about-us"')
header = header.replace('<body class="landing-page">', '<body>')
header = header.replace('href="styles.css"', 'href="../styles.css"')
footer = footer.replace('src="shopify-integration.js"', 'src="../shopify-integration.js"')
footer = footer.replace('src="script.js"', 'src="../script.js"')

full_page = header + about_html + footer

os.makedirs('about', exist_ok=True)
with open('about/index.html', 'w', encoding='utf-8') as f:
    f.write(full_page)
