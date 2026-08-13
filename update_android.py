import re
import os

gradle_path = 'c:/Users/legion-5pro/Documents/restie/admin-app/app/build.gradle.kts'
main_path = 'c:/Users/legion-5pro/Documents/restie/admin-app/app/src/main/java/com/example/restnestadmin/MainActivity.kt'

# 1. Update build.gradle.kts
with open(gradle_path, 'r', encoding='utf-8') as f:
    gradle = f.read()

if "retrofit2" not in gradle:
    deps = """
  // Retrofit & OkHttp
  implementation("com.squareup.retrofit2:retrofit:2.11.0")
  implementation("com.squareup.retrofit2:converter-gson:2.11.0")
  implementation("com.squareup.okhttp3:okhttp:4.12.0")
"""
    gradle = gradle.replace("dependencies {", "dependencies {" + deps)
    with open(gradle_path, 'w', encoding='utf-8') as f:
        f.write(gradle)
        print("Updated build.gradle.kts")

# 2. Add Retrofit Interface
api_client_code = """
package com.example.restnestadmin.api

import com.example.restnestadmin.Order
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Body
import retrofit2.http.Path

data class OrdersResponse(val success: Boolean, val orders: List<Order>)
data class BulkOrder(
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
)
data class BulkOrdersResponse(val success: Boolean, val bulkOrders: List<BulkOrder>)

interface RestNestApi {
    @GET("api/orders")
    suspend fun getOrders(): OrdersResponse

    @GET("api/bulk-orders")
    suspend fun getBulkOrders(): BulkOrdersResponse
}

object RetrofitClient {
    private const val BASE_URL = "https://restienestie.onrender.com/"
    
    val instance: RestNestApi by lazy {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        retrofit.create(RestNestApi::class.java)
    }
}
"""
os.makedirs('c:/Users/legion-5pro/Documents/restie/admin-app/app/src/main/java/com/example/restnestadmin/api', exist_ok=True)
with open('c:/Users/legion-5pro/Documents/restie/admin-app/app/src/main/java/com/example/restnestadmin/api/RetrofitClient.kt', 'w', encoding='utf-8') as f:
    f.write(api_client_code.strip())
print("Created RetrofitClient.kt")

# 3. Modify MainActivity.kt
with open(main_path, 'r', encoding='utf-8') as f:
    main_kt = f.read()

# Add imports
imports = """
import com.example.restnestadmin.api.RetrofitClient
import com.example.restnestadmin.api.BulkOrder
import kotlinx.coroutines.delay
"""
main_kt = main_kt.replace("import kotlinx.coroutines.flow.MutableStateFlow", "import kotlinx.coroutines.flow.MutableStateFlow\n" + imports)

# Update Order class to match MongoDB structure safely (or we can just map it when parsing).
# Actually Gson requires the fields to match or have @SerializedName. But we'll leave Order as is for now and just update the mapping if needed. But Gson mapping will fail if fields don't match. 
# Wait, let's just create a custom Order data class matching MongoDB inside the Retrofit response and then map it.
# It's safer to just replace the whole Firebase fetching block with Retrofit polling.

firebase_pattern = r'DisposableEffect\(refreshTrigger\).*?onDispose \{\s*registration\.remove\(\)\s*\}'
retrofit_polling = """
    LaunchedEffect(refreshTrigger) {
        while(true) {
            try {
                val response = RetrofitClient.instance.getOrders()
                if (response.success) {
                    val newOrders = response.orders.map { apiOrder -> 
                        Order(
                            id = apiOrder.id,
                            customerName = apiOrder.customerName ?: "",
                            address = apiOrder.address ?: "",
                            phone = apiOrder.phone ?: "",
                            amount = apiOrder.amount ?: 0.0,
                            items = apiOrder.items ?: "",
                            rawItems = apiOrder.rawItems ?: "[]",
                            status = apiOrder.status ?: "Placed",
                            date = apiOrder.date ?: "",
                            createdAt = apiOrder.createdAt ?: System.currentTimeMillis(),
                            paymentMethod = apiOrder.paymentMethod ?: "Unknown",
                            paymentId = apiOrder.paymentId ?: "N/A",
                            shiprocketAwb = apiOrder.shiprocketAwb ?: "N/A"
                        )
                    }
                    
                    val isFirst = isFirstSnapshotRef(null)
                    if (!isFirst && orders.isNotEmpty()) {
                        val oldIds = orders.map { it.id }.toSet()
                        newOrders.forEach { no ->
                            if (!oldIds.contains(no.id)) {
                                context.sendOrderNotification(no.id, no.customerName, no.amount)
                            }
                        }
                    }
                    isFirstSnapshotRef(false)
                    
                    orders.clear()
                    orders.addAll(newOrders)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
            delay(10000) // Poll every 10 seconds
        }
    }
"""
main_kt = re.sub(firebase_pattern, retrofit_polling.strip(), main_kt, flags=re.DOTALL)

# Add "Bulk" to tabs
main_kt = main_kt.replace('val tabs = listOf("Dashboard", "Orders", "Settings")', 'val tabs = listOf("Dashboard", "Orders", "Bulk", "Settings")')
main_kt = main_kt.replace('val icons = listOf(Icons.Filled.Home, Icons.Filled.List, Icons.Filled.Settings)', 'val icons = listOf(Icons.Filled.Home, Icons.Filled.List, Icons.Filled.ShoppingCart, Icons.Filled.Settings)')

# Add Bulk tab routing
bulk_routing = """
                        "Orders" -> OrdersTableScreen(
                            orders = orders,
                            onOrderClick = { selectedOrder = it },
                            onRefresh = { refreshTrigger++ },
                            onStatusChange = { order, newStatus ->
                                val idx = orders.indexOfFirst { it.id == order.id }
                                if (idx >= 0) {
                                    orders[idx] = orders[idx].copy(status = newStatus)
                                    scope.launch { updateOrderStatus(order.id, newStatus) }
                                }
                            },
                            colors = colors
                        )
                        "Bulk" -> BulkOrdersScreen(colors = colors)
"""
main_kt = re.sub(r'"Orders" -> OrdersTableScreen\([^)]*\)', bulk_routing.strip(), main_kt, flags=re.DOTALL)

# Add BulkOrdersScreen composable at the bottom
bulk_screen = """
// ──────────────────── BULK ORDERS ────────────────────
@Composable
fun BulkOrdersScreen(colors: AppColors) {
    var bulkOrders by remember { mutableStateOf<List<BulkOrder>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        while(true) {
            try {
                val response = RetrofitClient.instance.getBulkOrders()
                if (response.success) {
                    bulkOrders = response.bulkOrders
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
            isLoading = false
            delay(10000)
        }
    }

    Column(modifier = Modifier.fillMaxSize().padding(top = 48.dp, start = 16.dp, end = 16.dp)) {
        Text(text = "Bulk Requests", fontSize = 32.sp, fontWeight = FontWeight.ExtraBold, color = colors.textPrimary, modifier = Modifier.padding(bottom = 24.dp))
        
        if (isLoading && bulkOrders.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = colors.accent)
            }
        } else {
            LazyColumn {
                items(bulkOrders) { order ->
                    Box(modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp).clip(RoundedCornerShape(12.dp)).background(colors.cardBg).padding(16.dp)) {
                        Column {
                            Text("ID: ${order.id}", color = colors.accent, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Name: ${order.first_name} ${order.last_name}", color = colors.textPrimary)
                            Text("Email: ${order.email}", color = colors.textSecondary)
                            Text("Phone: ${order.phone}", color = colors.textSecondary)
                            Text("Status: ${order.status}", color = if(order.status == "Pending") Color(0xFFFFC107) else Color(0xFF4CAF50), fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}
"""
main_kt += "\n" + bulk_screen

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(main_kt)

print("Updated MainActivity.kt")
