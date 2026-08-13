import re

file_path = 'c:/Users/legion-5pro/Documents/restie/server/index.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add BulkOrder schema
bulk_schema_code = """
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
"""

if "const BulkOrder = mongoose.model" not in content:
    content = content.replace("const Order = mongoose.model('Order', orderSchema);", 
                              "const Order = mongoose.model('Order', orderSchema);\n" + bulk_schema_code)

# 2. Add API endpoints
endpoints_code = """
// ----------------------------------------------------
// Endpoints for Mobile Admin App
// ----------------------------------------------------
app.get('/api/orders', async (req, res) => {
    try {
        const orders = await Order.find().sort({ created_at: -1 });
        res.json({ success: true, orders });
    } catch (error) {
        console.error('Error fetching orders:', error);
        res.status(500).json({ success: false, error: 'Failed to fetch orders' });
    }
});

app.get('/api/bulk-orders', async (req, res) => {
    try {
        const bulkOrders = await BulkOrder.find().sort({ created_at: -1 });
        res.json({ success: true, bulkOrders });
    } catch (error) {
        console.error('Error fetching bulk orders:', error);
        res.status(500).json({ success: false, error: 'Failed to fetch bulk orders' });
    }
});

app.post('/api/bulk-orders', async (req, res) => {
    try {
        const orderData = req.body;
        const newBulkOrder = new BulkOrder({
            id: `BULK_${Date.now()}`,
            ...orderData
        });
        await newBulkOrder.save();
        res.json({ success: true, order: newBulkOrder });
    } catch (error) {
        console.error('Error saving bulk order:', error);
        res.status(500).json({ success: false, error: 'Failed to save bulk order' });
    }
});

"""

if "/api/bulk-orders" not in content:
    # insert before app.listen or at the end
    content = content.replace("app.listen(port", endpoints_code + "\napp.listen(port")
    
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Server endpoints added successfully!")
