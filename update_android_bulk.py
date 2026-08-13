import os
import re

app_dir = 'c:/Users/legion-5pro/Documents/restie/admin-app/app/src/main/java/com/example/restnestadmin'
retrofit_kt = os.path.join(app_dir, 'api', 'RetrofitClient.kt')
main_kt = os.path.join(app_dir, 'MainActivity.kt')

# 1. Update RetrofitClient.kt
with open(retrofit_kt, 'r', encoding='utf-8') as f:
    r_content = f.read()

r_old = """data class BulkOrder(
    val id: String,
    val first_name: String,
    val last_name: String,
    val email: String,
    val phone: String,
    val address: String,
    val city: String,
    val state: String,
    val pincode: String,
    val status: String,
    val created_at: String
)"""

r_new = """data class BulkOrder(
    val id: String,
    val first_name: String,
    val last_name: String,
    val email: String,
    val phone: String,
    val business_name: String,
    val quantity: Int,
    val status: String,
    val created_at: String
)"""

r_content = r_content.replace(r_old, r_new)

with open(retrofit_kt, 'w', encoding='utf-8') as f:
    f.write(r_content)


# 2. Update MainActivity.kt
with open(main_kt, 'r', encoding='utf-8') as f:
    m_content = f.read()

m_old = """                            Text("Name: ${order.first_name} ${order.last_name}", color = colors.textPrimary)
                            Text("Email: ${order.email}", color = colors.textSecondary)
                            Text("Phone: ${order.phone}", color = colors.textSecondary)
                            Text("Status: ${order.status}", color = if(order.status == "Pending") Color(0xFFFFC107) else Color(0xFF4CAF50), fontWeight = FontWeight.Bold)"""

m_new = """                            Text("Business: ${order.business_name}", color = colors.textPrimary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Text("Qty: ${order.quantity}", color = colors.accent, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Name: ${order.first_name} ${order.last_name}", color = colors.textPrimary)
                            Text("Email: ${order.email}", color = colors.textSecondary)
                            Text("Phone: ${order.phone}", color = colors.textSecondary)
                            Text("Status: ${order.status}", color = if(order.status == "Pending") Color(0xFFFFC107) else Color(0xFF4CAF50), fontWeight = FontWeight.Bold)"""

m_content = m_content.replace(m_old, m_new)

with open(main_kt, 'w', encoding='utf-8') as f:
    f.write(m_content)

print("Updated RetrofitClient.kt and MainActivity.kt")
