import os
import glob
import re

# 1. Update Navigation Bar in all HTML files
html_files = glob.glob('c:/Users/legion-5pro/Documents/restie/**/*.html', recursive=True)

for file_path in html_files:
    if 'server' in file_path or 'node_modules' in file_path:
        continue
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-16') as f:
            html = f.read()
            
    # Add Bulk link after Cushion if it doesn't exist
    if 'id="nav-bulk"' not in html:
        # Regex to find Cushion link and capture its prefix (like "../" or "")
        pattern = r'(<li>\s*<a class="main-nav__link" href="([^"]*)cushions/?" id="nav-cushion">Cushion</a>\s*</li>)'
        
        def replace_func(match):
            original = match.group(1)
            prefix = match.group(2)
            new_link = f'\n<li><a class="main-nav__link" href="{prefix}bulk/" id="nav-bulk">Bulk</a></li>'
            return original + new_link
            
        new_html = re.sub(pattern, replace_func, html)
        
        if new_html != html:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_html)

# 2. Create bulk/index.html
os.makedirs('c:/Users/legion-5pro/Documents/restie/bulk', exist_ok=True)

with open('c:/Users/legion-5pro/Documents/restie/checkout.html', 'r', encoding='utf-8') as f:
    checkout_html = f.read()

# Fix CSS paths
bulk_html = checkout_html.replace('href="styles.css', 'href="../styles.css')
bulk_html = bulk_html.replace('href="new_styles.css', 'href="../new_styles.css')
bulk_html = bulk_html.replace('src="assets/', 'src="../assets/')
bulk_html = bulk_html.replace('href="assets/', 'href="../assets/')
bulk_html = bulk_html.replace('href="index.html"', 'href="../index.html"')

# Change Title
bulk_html = bulk_html.replace('<title>Checkout – RestNest</title>', '<title>Bulk Orders – RestNest</title>')
bulk_html = bulk_html.replace('<span class="current">Checkout</span>', '<span class="current">Bulk Orders</span>')

# Remove Razorpay and Checkout scripts
bulk_html = re.sub(r'<script src="https://checkout\.razorpay\.com/v1/checkout\.js"></script>', '', bulk_html)
bulk_html = re.sub(r'<script src="checkout\.js"></script>', '', bulk_html)
bulk_html = re.sub(r'<script src="../checkout\.js"></script>', '', bulk_html)

# Change "Shipping Details" to "Order Information"
bulk_html = bulk_html.replace('Shipping Details', 'Order Information')

# Remove the Order Summary Column
# The column starts with <div class="checkout-summary-col"> and ends before </div> </div> <!-- footer -->
summary_pattern = r'<!-- Right: Order Summary \(sticky\) -->.*?</div>\s*</div>'
bulk_html = re.sub(summary_pattern, '', bulk_html, flags=re.DOTALL)

# Update the grid layout to be 1 column centered
grid_pattern = r'\.checkout-container \{\s*max-width: 1080px;\s*margin: 0 auto;\s*padding: 0 1\.5rem;\s*display: grid;\s*grid-template-columns: minmax\(0, 1\.1fr\) minmax\(0, 0\.9fr\);'
new_grid = """.checkout-container {
            max-width: 700px;
            margin: 0 auto;
            padding: 0 1.5rem;
            display: grid;
            grid-template-columns: 1fr;"""
bulk_html = re.sub(grid_pattern, new_grid, bulk_html)

# Add a submit button at the bottom of the form since we removed the pay button
submit_btn_html = """
                    <button type="submit" class="pay-btn" style="margin-top: 2rem;">
                        Submit Bulk Request
                        <span class="btn-icon">→</span>
                    </button>
"""
bulk_html = bulk_html.replace('</form>', submit_btn_html + '\n                </form>')

with open('c:/Users/legion-5pro/Documents/restie/bulk/index.html', 'w', encoding='utf-8') as f:
    f.write(bulk_html)

print("Bulk page created and navigation updated.")
