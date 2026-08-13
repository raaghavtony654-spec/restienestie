import re
import os

base_dir = 'c:/Users/legion-5pro/Documents/restie'
bulk_html = os.path.join(base_dir, 'bulk/index.html')

with open(bulk_html, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace address, city, state, pincode with Business Name and Quantity
pattern_address = r'<div class="form-group">\s*<label for="address">Full Address</label>.*?</div>\s*</div>'
replacement_address = """
                    <div class="form-row">
                        <div class="form-group">
                            <label for="businessName">Business Name</label>
                            <input type="text" id="businessName" required placeholder="Your Business Name">
                            <span class="input-highlight"></span>
                        </div>
                        <div class="form-group">
                            <label for="quantity">Quantity (Min 15)</label>
                            <input type="number" id="quantity" required min="15" placeholder="15">
                            <span class="input-highlight"></span>
                        </div>
                    </div>
"""
content = re.sub(pattern_address, replacement_address.strip(), content, flags=re.DOTALL)

# 2. Replace the checkout script with a custom bulk submit script
script_pattern = r'<script type="module" src="checkout.js\?v=6"></script>'
custom_script = """
    <script>
        document.querySelector('form').addEventListener('submit', async (e) => {
            // Check if it's the footer form or checkout form
            if (e.target.classList.contains('footer-subscribe')) return;
            
            e.preventDefault();
            const btn = e.target.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.innerHTML = 'Submitting...';

            const payload = {
                first_name: document.getElementById('fname').value,
                last_name: document.getElementById('lname').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                business_name: document.getElementById('businessName').value,
                quantity: document.getElementById('quantity').value
            };

            try {
                const res = await fetch('https://restienestie.onrender.com/api/bulk-orders', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (data.success) {
                    alert('Thank you! Your bulk order request has been submitted successfully.');
                    e.target.reset();
                } else {
                    alert('Error: ' + (data.error || 'Failed to submit request.'));
                }
            } catch (err) {
                console.error(err);
                alert('Network error. Please try again.');
            } finally {
                btn.disabled = false;
                btn.innerHTML = 'Submit Bulk Request <span class="btn-icon"> </span>';
            }
        });
    </script>
"""
content = re.sub(script_pattern, custom_script, content)

# 3. Form id update just in case (optional, but it uses querySelector('form') above, which is fine since the other form has class 'footer-subscribe')

with open(bulk_html, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated bulk/index.html")
