require('dotenv').config();
const express = require('express');
const cors = require('cors');
const crypto = require('crypto');
const Razorpay = require('razorpay');
const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const { open } = require('sqlite');

const app = express();
app.use(cors());
app.use(express.json());

let db;
(async () => {
    db = await open({
        filename: './orders.db',
        driver: sqlite3.Database
    });
    await db.exec(`
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            customer_name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            total_amount REAL,
            items TEXT,
            status TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    `);
})();

// ----------------------------------------------------
// Configuration
// ----------------------------------------------------
const RAZORPAY_KEY_ID = process.env.RAZORPAY_KEY_ID || 'dummy_key_id';
const RAZORPAY_KEY_SECRET = process.env.RAZORPAY_KEY_SECRET || 'dummy_secret';

const razorpay = new Razorpay({
    key_id: RAZORPAY_KEY_ID,
    key_secret: RAZORPAY_KEY_SECRET,
});

let shiprocketToken = null;

// ----------------------------------------------------
// Helper: Authenticate with Shiprocket
// ----------------------------------------------------
async function getShiprocketToken() {
    if (shiprocketToken) return shiprocketToken;

    if (!process.env.SHIPROCKET_EMAIL || !process.env.SHIPROCKET_PASSWORD) {
        console.warn('Shiprocket credentials missing. Using mock token.');
        return 'MOCK_TOKEN';
    }

    try {
        const response = await axios.post('https://apiv2.shiprocket.in/v1/external/auth/login', {
            email: process.env.SHIPROCKET_EMAIL,
            password: process.env.SHIPROCKET_PASSWORD,
        });
        shiprocketToken = response.data.token;
        return shiprocketToken;
    } catch (error) {
        console.error('Shiprocket auth failed:', error.response ? error.response.data : error.message);
        throw new Error('Failed to authenticate with Shiprocket');
    }
}

// ----------------------------------------------------
// Endpoint 1: Create Razorpay Order
// ----------------------------------------------------
app.get('/api/config', (req, res) => {
    res.json({ razorpayKeyId: RAZORPAY_KEY_ID });
});

app.post('/api/create-order', async (req, res) => {
    try {
        const { amount, currency = 'INR', receipt } = req.body;

        if (RAZORPAY_KEY_ID === 'dummy_key_id') {
            console.warn('Using dummy Razorpay keys. Returning mock order.');
            return res.json({ 
                success: true, 
                order: {
                    id: `order_mock_${Date.now()}`,
                    amount: amount * 100,
                    currency
                } 
            });
        }

        const options = {
            amount: amount * 100, // amount in the smallest currency unit (paise)
            currency,
            receipt: receipt || `receipt_${Date.now()}`
        };

        const order = await razorpay.orders.create(options);
        res.json({ success: true, order });
    } catch (error) {
        console.error('Error creating Razorpay order:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

// ----------------------------------------------------
// Endpoint 2: Verify Razorpay Payment Signature
// ----------------------------------------------------
app.post('/api/verify-payment', (req, res) => {
    try {
        const { razorpay_order_id, razorpay_payment_id, razorpay_signature, is_mock } = req.body;

        if (RAZORPAY_KEY_SECRET === 'dummy_secret' || is_mock) {
            console.warn('Bypassing signature verification for mock/test flow.');
            return res.status(200).json({ success: true, message: "Mock payment verified successfully" });
        }

        const sign = razorpay_order_id + "|" + razorpay_payment_id;
        const expectedSign = crypto
            .createHmac("sha256", RAZORPAY_KEY_SECRET)
            .update(sign.toString())
            .digest("hex");

        if (razorpay_signature === expectedSign) {
            return res.status(200).json({ success: true, message: "Payment verified successfully" });
        } else {
            return res.status(400).json({ success: false, message: "Invalid signature sent!" });
        }
    } catch (error) {
        console.error('Error verifying payment:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

// ----------------------------------------------------
// Endpoint 3: Create Shiprocket Shipment
// ----------------------------------------------------
app.post('/api/create-shipment', async (req, res) => {
    try {
        const { orderData } = req.body;
        // orderData should contain billing_customer_name, billing_address, order_items, etc.

        // Default order format for Shiprocket
        const shiprocketOrderPayload = {
            order_id: orderData.order_id || `ORDER_${Date.now()}`,
            order_date: new Date().toISOString(),
            pickup_location: "Primary", // Must match your Shiprocket pickup location name
            billing_customer_name: orderData.name,
            billing_last_name: "",
            billing_address: orderData.address,
            billing_city: orderData.city,
            billing_pincode: orderData.pincode,
            billing_state: orderData.state,
            billing_country: "India",
            billing_email: orderData.email,
            billing_phone: orderData.phone,
            shipping_is_billing: true,
            order_items: orderData.items.map(item => ({
                name: item.name,
                sku: item.sku || "SKU-DEFAULT",
                units: item.quantity,
                selling_price: item.price,
                discount: 0,
                tax: 0,
                hsn: ""
            })),
            payment_method: "Prepaid",
            sub_total: orderData.total_amount,
            length: 10, // Default package dimensions (cm) - should ideally come from products
            breadth: 10,
            height: 10,
            weight: 1 // Default package weight (kg)
        };

        const token = await getShiprocketToken();
        
        let responseData;
        if (token === 'MOCK_TOKEN') {
            console.warn('Simulating Shiprocket order creation.');
            responseData = {
                order_id: shiprocketOrderPayload.order_id,
                shipment_id: `SHIP_${Math.floor(Math.random() * 1000000)}`,
                status: 'NEW',
                status_code: 1,
                awb_code: `AWB${Math.floor(Math.random() * 1000000000)}`
            };
        } else {
            const response = await axios.post(
                'https://apiv2.shiprocket.in/v1/external/orders/create/adhoc',
                shiprocketOrderPayload,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            responseData = response.data;
        }

        // Save order to SQLite database for the Admin app
        await db.run(
            `INSERT INTO orders (id, customer_name, email, phone, address, total_amount, items, status) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                orderData.order_id, 
                orderData.name, 
                orderData.email, 
                orderData.phone, 
                `${orderData.address}, ${orderData.city}, ${orderData.state} - ${orderData.pincode}`,
                orderData.total_amount,
                JSON.stringify(orderData.items),
                'Placed'
            ]
        );

        res.json({ success: true, data: responseData });
    } catch (error) {
        console.error('Error creating Shiprocket order:', error.response ? error.response.data : error.message);
        res.status(500).json({ success: false, error: 'Failed to create shipment' });
    }
});

const PORT = process.env.PORT || 3000;

// ----------------------------------------------------
// Endpoint 4: Get All Orders (For Admin App)
// ----------------------------------------------------
app.get('/api/orders', async (req, res) => {
    try {
        const orders = await db.all('SELECT * FROM orders ORDER BY created_at DESC');
        // Parse items JSON back into objects for the frontend
        orders.forEach(order => {
            if (order.items) {
                try {
                    order.items = JSON.parse(order.items);
                } catch(e) {}
            }
        });
        res.json({ success: true, orders });
    } catch (error) {
        console.error('Error fetching orders:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

// ----------------------------------------------------
// Endpoint 5: Place Order Directly (Bypass Razorpay)
// ----------------------------------------------------
app.post('/api/place-order-test', async (req, res) => {
    try {
        const { orderData } = req.body;
        
        await db.run(
            `INSERT INTO orders (id, customer_name, email, phone, address, total_amount, items, status) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                orderData.id, 
                orderData.customer_name, 
                orderData.email, 
                orderData.phone, 
                orderData.address,
                orderData.total_amount,
                JSON.stringify(orderData.items),
                'Placed'
            ]
        );
        res.json({ success: true, message: 'Order placed successfully' });
    } catch (error) {
        console.error('Error placing order:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

// ----------------------------------------------------
// Endpoint 6: Update Order Status
// ----------------------------------------------------
app.post('/api/update-order-status', async (req, res) => {
    try {
        const { id, status } = req.body;
        await db.run(`UPDATE orders SET status = ? WHERE id = ?`, [status, id]);
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

// ----------------------------------------------------
// Endpoint 7: Delete Order
// ----------------------------------------------------
app.delete('/api/delete-order/:id', async (req, res) => {
    try {
        await db.run(`DELETE FROM orders WHERE id = ?`, [req.params.id]);
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

// ----------------------------------------------------
// Endpoint 8: Reset Orders
// ----------------------------------------------------
app.delete('/api/reset-orders', async (req, res) => {
    try {
        await db.run(`DELETE FROM orders`);
        res.json({ success: true, message: 'All orders deleted' });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
