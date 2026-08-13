import re

terms_file = 'c:/Users/legion-5pro/Documents/restie/terms/index.html'

with open(terms_file, 'r', encoding='utf-8') as f:
    content = f.read()

new_html = """    <div class="terms-container">
        <h1>About RestNest</h1>
        
        <h2>Where Comfort Meets Timeless Design</h2>
        <p>At RestNest, we believe that better rest begins with the right comfort. We create thoughtfully designed pillows that combine softness, support, quality, and modern aesthetics—helping you turn every night and every moment of relaxation into a more comfortable experience.</p>
        <p>Whether you're looking for better support while you sleep, a cozy addition to your bedroom, or simply a pillow that feels as good as it looks, RestNest brings comfort and thoughtful design together for modern homes.</p>

        <h2>Our Story</h2>
        <p><em>Every great day begins with a good night's rest.</em></p>
        <p>RestNest was founded with a simple vision—to make premium-quality pillows accessible without compromising on comfort, design, or craftsmanship.</p>
        <p>We carefully select materials and thoughtfully develop every product to provide the perfect balance of softness and support. From everyday sleeping pillows to comfort-focused designs, each RestNest product is created with attention to detail and the needs of modern lifestyles in mind.</p>

        <h2>Our Mission</h2>
        <p>Our mission is to make everyday rest more comfortable by creating pillows that combine thoughtful design, quality materials, and dependable comfort.</p>
        <p>We strive to deliver products that help people sleep, relax, and unwind better while providing a simple and enjoyable shopping experience from selection to delivery.</p>

        <h2>Our Vision</h2>
        <p>To become one of India's most trusted pillow and sleep-comfort brands by creating innovative, high-quality products that make better rest a part of everyday life.</p>

        <h2>What Makes Us Different</h2>
        <h3>Premium Comfort</h3>
        <p>Every pillow is thoughtfully designed using carefully selected materials to deliver lasting softness, comfort, and support.</p>
        
        <h3>Thoughtful Design</h3>
        <p>Our pillows are designed to complement modern lifestyles and bedrooms while focusing on what matters most—your comfort.</p>

        <h3>Quality You Can Trust</h3>
        <p>We pay close attention to materials, construction, and finishing to ensure every RestNest pillow meets our standards for quality and durability.</p>

        <h3>Customer-Centric Experience</h3>
        <p>From choosing the right pillow to delivery and after-sales support, we're committed to making your RestNest experience simple, transparent, and enjoyable.</p>

        <h2>Our Values</h2>
        <ul>
            <li><strong>Comfort First</strong> – We believe quality rest should be comfortable, relaxing, and accessible.</li>
            <li><strong>Quality Without Compromise</strong> – We carefully select materials and maintain high standards across every product.</li>
            <li><strong>Customer Commitment</strong> – Your comfort and satisfaction are at the heart of everything we do.</li>
            <li><strong>Innovation</strong> – We continuously explore better designs and materials to improve your everyday rest.</li>
            <li><strong>Responsible Choices</strong> – We strive to make thoughtful choices in our sourcing, manufacturing, and packaging.</li>
        </ul>

        <h2>Bringing Comfort Home</h2>
        <p>A pillow is more than just something you sleep on. It's where your head rests after a long day, where you unwind with a book, and where comfort becomes part of your daily routine.</p>
        <p>At RestNest, we're proud to be part of those everyday moments by creating pillows that bring together thoughtful design, dependable quality, and lasting comfort.</p>

        <h2>Build Your Perfect Rest with RestNest</h2>
        <p>Discover pillows designed to elevate your everyday comfort with softness, support, and timeless style. Explore the RestNest collection and find the comfort that makes your space—and your rest—feel truly like home.</p>
    </div>"""

# Replace between <div class="terms-container"> and the matching </div> before <!-- ===== FOOTER ===== -->
# Use a regex that matches from <div class="terms-container"> up to </div>\s*<!-- ===== FOOTER ===== -->
pattern = r'<div class="terms-container">.*?</div>(?=\s*<!-- ===== FOOTER ===== -->)'

new_content = re.sub(pattern, new_html, content, flags=re.DOTALL)

with open(terms_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated terms/index.html")
