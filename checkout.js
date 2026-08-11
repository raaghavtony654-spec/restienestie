/**
 * RestNest - Custom Checkout Integration (Razorpay + Shiprocket)
 */

const BACKEND_URL = 'http://localhost:3000/api'; // Change for production

// ----------------------------------------------------
// UI Initialization
// ----------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    // Only run on checkout page
    if (document.getElementById('checkout-form')) {
        initCheckoutPage();
    }
});

function formatPrice(num) {
    return 'Rs. ' + parseFloat(num).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function initCheckoutPage() {
    const cart = JSON.parse(localStorage.getItem('restnest_cart')) || [];
    
    if (cart.length === 0) {
        alert('Your cart is empty!');
        window.location.href = 'index.html';
        return;
    }

    const itemsContainer = document.getElementById('checkout-items');
    const subtotalEl = document.getElementById('summary-subtotal');
    const totalEl = document.getElementById('summary-total');
    
    let totalAmount = 0;

    itemsContainer.innerHTML = '';
    
    cart.forEach(item => {
        totalAmount += (item.price * item.quantity);
        
        const div = document.createElement('div');
        div.className = 'checkout-item';
        div.innerHTML = `
            <img src="${item.img}" alt="${item.name}">
            <div class="checkout-item-details">
                <div class="checkout-item-title">${item.name}</div>
                <div class="checkout-item-price">Qty: ${item.quantity} × ${formatPrice(item.price)}</div>
            </div>
            <div style="font-weight: 500;">${formatPrice(item.price * item.quantity)}</div>
        `;
        itemsContainer.appendChild(div);
    });

    subtotalEl.textContent = formatPrice(totalAmount);
    totalEl.textContent = formatPrice(totalAmount);

    // Form Submission Handler
    const form = document.getElementById('checkout-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const customerInfo = {
            name: `${document.getElementById('fname').value} ${document.getElementById('lname').value}`.trim(),
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            address: document.getElementById('address').value,
            city: document.getElementById('city').value,
            state: document.getElementById('state').value,
            pincode: document.getElementById('pincode').value
        };

        await processCheckout(cart, totalAmount, customerInfo);
    });
}

function showStatus(message, type) {
    const statusEl = document.getElementById('checkout-status');
    if (!statusEl) return;
    
    statusEl.textContent = message;
    statusEl.className = `status-${type}`;
    statusEl.style.display = 'block';
}

// ----------------------------------------------------
// Checkout Flow (Razorpay -> Shiprocket)
// ----------------------------------------------------
async function processCheckout(cart, totalAmount, customerInfo) {
    const payBtn = document.getElementById('pay-btn');
    payBtn.disabled = true;
    payBtn.textContent = 'Placing Order...';
    showStatus('Processing your order...', 'loading');

    const orderData = {
        id: 'ORD' + Date.now().toString().slice(-6),
        customer_name: customerInfo.name,
        email: customerInfo.email,
        phone: customerInfo.phone,
        address: `${customerInfo.address}, ${customerInfo.city}, ${customerInfo.state} - ${customerInfo.pincode}`,
        total_amount: totalAmount,
        items: cart.map(item => ({
            name: item.name,
            quantity: item.quantity,
            price: item.price
        }))
    };

    try {
        const res = await fetch(`${BACKEND_URL}/place-order-test`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ orderData })
        });
        
        const data = await res.json();
        
        if (!data.success) throw new Error('Failed to place order');

        // Clear cart
        localStorage.removeItem('restnest_cart');
        showStatus('Order placed successfully! Redirecting...', 'success');

        setTimeout(() => {
            alert('Order #' + orderData.id + ' placed successfully! Thank you for shopping with RestNest.');
            window.location.href = 'index.html';
        }, 1500);

    } catch (err) {
        console.error(err);
        showStatus('Error placing order. Please try again.', 'error');
        payBtn.disabled = false;
        payBtn.textContent = 'Place Order';
    }
}
