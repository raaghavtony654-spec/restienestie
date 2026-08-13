require('dotenv').config();
const express = require('express');
const cors = require('cors');
const crypto = require('crypto');
const Razorpay = require('razorpay');
const axios = require('axios');
const mongoose = require('mongoose');

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB Connection
const MONGODB_URI = process.env.MONGODB_URI;

if (!MONGODB_URI) {
    console.warn('WARNING: MONGODB_URI is not set. Using local database for testing.');
}

mongoose.connect(MONGODB_URI || 'mongodb://localhost:27017/restnest')
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('MongoDB connection error:', err));

// Mongoose Schema
const orderSchema = new mongoose.Schema({
    id: { type: String, required: true, unique: true },
    customer_name: String,
    email: String,
    phone: String,
    address: String,
    total_amount: Number,
    items: mongoose.Schema.Types.Mixed,
    status: String,
    created_at: { type: Date, default: Date.now }
});

const Order = mongoose.model('Order', orderSchema);

const bulkOrderSchema = new mongoose.Schema({
    id: { type: String, required: true, unique: true },
    first_name: String,
    last_name: String,
    email: String,
    phone: String,
    address: String,
    city: String,
    state: String,
    pincode: String,
    status: { type: String, default: 'Pending' },
    created_at: { type: Date, default: Date.now }
});

const BulkOrder = mongoose.model('BulkOrder', bulkOrderSchema);

const pageTrafficSchema = new mongoose.Schema({
    page: { type: String, required: true, unique: true },
    visits: { type: Number, default: 0 }
});

const PageTraffic = mongoose.model('PageTraffic', pageTrafficSchema);


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
            amount: amount * 100,
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

        const shiprocketOrderPayload = {
            order_id: orderData.order_id || `ORDER_${Date.now()}`,
            order_date: new Date().toISOString(),
            pickup_location: "Primary",
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
            length: 10,
            breadth: 10,
            height: 10,
            weight: 1
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

        // Save order to MongoDB
        const newOrder = new Order({
            id: orderData.order_id,
            customer_name: orderData.name,
            email: orderData.email,
            phone: orderData.phone,
            address: `${orderData.address}, ${orderData.city}, ${orderData.state} - ${orderData.pincode}`,
            total_amount: orderData.total_amount,
            items: orderData.items,
            status: 'Placed'
        });
        await newOrder.save();

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
        const orders = await Order.find().sort({ created_at: -1 });
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
        
        const newOrder = new Order({
            id: orderData.id,
            customer_name: orderData.customer_name,
            email: orderData.email,
            phone: orderData.phone,
            address: orderData.address,
            total_amount: orderData.total_amount,
            items: orderData.items,
            status: 'Placed'
        });
        await newOrder.save();

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
        await Order.updateOne({ id }, { status });
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
        await Order.deleteOne({ id: req.params.id });
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
        await Order.deleteMany({});
        res.json({ success: true, message: 'All orders deleted' });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});


// ----------------------------------------------------
// Bulk Orders Endpoints
// ----------------------------------------------------
app.post('/api/bulk-orders', async (req, res) => {
    try {
        const { first_name, last_name, email, phone, business_name, quantity } = req.body;
        const newBulkOrder = new BulkOrder({
            id: `bulk_${Date.now()}_${Math.floor(Math.random() * 1000)}`,
            first_name,
            last_name,
            email,
            phone,
            business_name,
            quantity: Number(quantity)
        });
        await newBulkOrder.save();
        res.json({ success: true, bulkOrder: newBulkOrder });
    } catch (error) {
        console.error('Error creating bulk order:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

app.get('/api/bulk-orders', async (req, res) => {
    try {
        const bulkOrders = await BulkOrder.find().sort({ created_at: -1 });
        res.json({ success: true, bulkOrders });
    } catch (error) {
        console.error('Error fetching bulk orders:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

// ----------------------------------------------------
// Page Traffic Endpoints
// ----------------------------------------------------
app.post('/api/track-page', async (req, res) => {
    try {
        const { page } = req.body;
        if (!page) return res.status(400).json({ success: false, error: 'Page name required' });
        
        await PageTraffic.findOneAndUpdate(
            { page },
            { $inc: { visits: 1 } },
            { upsert: true, new: true }
        );
        res.json({ success: true });
    } catch (error) {
        console.error('Error tracking page:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

app.get('/api/page-traffic', async (req, res) => {
    try {
        const traffic = await PageTraffic.find();
        res.json({ success: true, traffic });
    } catch (error) {
        console.error('Error fetching traffic:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

app.post('/api/reset-traffic', async (req, res) => {
    try {
        await PageTraffic.deleteMany({});
        res.json({ success: true });
    } catch (error) {
        console.error('Error resetting traffic:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
