import os
import re

server_js = 'c:/Users/legion-5pro/Documents/restie/server/index.js'

with open(server_js, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add bulkOrderSchema and Model
if 'const bulkOrderSchema' not in content:
    schema_code = """
const bulkOrderSchema = new mongoose.Schema({
    id: { type: String, required: true, unique: true },
    first_name: String,
    last_name: String,
    email: String,
    phone: String,
    business_name: String,
    quantity: Number,
    status: { type: String, default: 'Pending' },
    created_at: { type: Number, default: () => Date.now() }
});
const BulkOrder = mongoose.model('BulkOrder', bulkOrderSchema);
"""
    # Insert right after const Order = mongoose.model('Order', orderSchema);
    content = re.sub(r"const Order = mongoose\.model\('Order', orderSchema\);", r"const Order = mongoose.model('Order', orderSchema);\n" + schema_code, content)

# 2. Add endpoints POST /api/bulk-orders and GET /api/bulk-orders
if "app.post('/api/bulk-orders'" not in content:
    endpoints = """
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
"""
    # Append to the end of the file before app.listen if it exists, or just append
    if 'app.listen(PORT' in content:
        content = content.replace('app.listen(PORT', endpoints + '\napp.listen(PORT')
    else:
        content += '\n' + endpoints

with open(server_js, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated server/index.js")
