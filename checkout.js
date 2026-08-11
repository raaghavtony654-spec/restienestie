/**
 * RestNest - Custom Checkout Integration (Razorpay + Shiprocket)
 */

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getFirestore, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "[HIDDEN_FIREBASE_KEY]",
  authDomain: "restnest-355b3.firebaseapp.com",
  projectId: "restnest-355b3",
  storageBucket: "restnest-355b3.firebasestorage.app",
  messagingSenderId: "418459690953",
  appId: "1:418459690953:web:61db69e9b41a0e54a3aa18",
  measurementId: "G-Q1EJ31CTXC"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

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
        // Save order to Firestore
        await addDoc(collection(db, "orders"), {
            ...orderData,
            createdAt: serverTimestamp()
        });

        // Also save to localStorage for fallback if needed
        const existingOrders = JSON.parse(localStorage.getItem('restnest_orders') || '[]');
        existingOrders.push(orderData);
        localStorage.setItem('restnest_orders', JSON.stringify(existingOrders));

        // Simulate network delay
        setTimeout(() => {
            showStatus('Order placed successfully! Redirecting...', 'success');
            localStorage.removeItem('restnest_cart');
            
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        }, 1500);

    } catch (error) {
        console.error('Checkout error:', error);
        showStatus('Error placing the order. Please try again.', 'error');
        payBtn.disabled = false;
        payBtn.textContent = 'Place Order';
    }
}
